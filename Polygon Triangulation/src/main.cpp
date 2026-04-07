#include <raylib.h>
#include <iostream>
#include <fstream>
#include <raymath.h>
#include <vector>
#include <set>
#include <tuple>
#include <string> 
#include <ctime>
#include <array>
#include <algorithm>
#include <queue>
#include <list>

using namespace std;

enum Side {LEFT, RIGHT};
enum Type {START, END, SPLIT, MERGE, REGULAR};

struct MonoPoint {
    Vector2 Point; 
    Side Side;
};

struct PolyPoint {
        Vector2 Point;
        Type Type;
        Vector2 Next_Point;
        Vector2 Last_Point;
        int Index;
    };

struct ComparePolyY {
    bool operator()(PolyPoint a, PolyPoint b){
        return a.Point.y>b.Point.y;
    }
};
struct CompareMonoY {
    bool operator()(MonoPoint a, MonoPoint b){
        return a.Point.y>b.Point.y;
    }
};

struct edge {
    array<Vector2,2> Edge;
    PolyPoint Helper;
    int Index;
};

int find_left_intersect(vector<edge> T, PolyPoint Vi){
    int closest = -1;
    float max_x;
    for (int j=0; j<(int)T.size(); j++){
        Vector2 a = T[j].Edge[0];
        Vector2 b = T[j].Edge[1];

        float x_intersect = b.x+(Vi.Point.y-b.y)*(a.x-b.x)/(a.y-b.y);

        if (closest==-1 && x_intersect<Vi.Point.x){
            max_x = x_intersect;
            closest = j;
        } else {
            if (x_intersect>max_x && x_intersect<Vi.Point.x){
                max_x = x_intersect;
                closest = j;
            }
        }
    }
    return closest;
}

vector<array<int,2>> Add_Edges(vector<Vector2> Points){

    priority_queue<PolyPoint, vector<PolyPoint>, ComparePolyY> Q;

    for (int i=0; i<(int)Points.size(); i++){
        PolyPoint Point;

        Point.Point=Points[i];
        Point.Index = i;

        Point.Last_Point = Points[(Points.size()+i-1)%Points.size()];
        Point.Next_Point = Points[(Points.size()+i+1)%Points.size()];

        Vector2 p = Point.Point;
        Vector2 q = Point.Next_Point;
        Vector2 r = Point.Last_Point;
        if (((q.x-p.x)*(r.y-p.y)) - ((r.x-p.x)*(q.y-p.y)) > 0){
            if (p.y>q.y && p.y>r.y){
                Point.Type = END;
            } else if (p.y<q.y && p.y<r.y){
                Point.Type = START;
            } else {
                Point.Type = REGULAR;
            }
        } else {
            if (p.y>q.y && p.y>r.y){
                Point.Type = MERGE;
            } else if (p.y<q.y && p.y<r.y){
                Point.Type = SPLIT;
            } else {
                Point.Type = REGULAR;
            }
        }

        Q.push(Point);
    }

    vector<edge> T;

    vector<array<int,2>> New_Edges;

    while (!Q.empty()){
        PolyPoint Vi = Q.top();
        edge ei;

        ei.Edge={Vi.Point,Vi.Last_Point};
        ei.Helper=Vi;
        ei.Index = Vi.Index;

        int closest;
        switch(Vi.Type){
            
            case START:
                T.push_back(ei);
                break;

            case END:

                for (int i=0; i<(int)T.size(); i++){
                    if (T[i].Index == (int)(Vi.Index+1)%(int)Points.size()){
                        if (T[i].Helper.Type==MERGE){
                            New_Edges.push_back({Vi.Index,T[i].Helper.Index});
                        }
                        T.erase(T.begin() + i);
                        break;
                    }
                }
                break;

            case SPLIT:
 
                closest = find_left_intersect(T, Vi);

                New_Edges.push_back({Vi.Index,T[closest].Helper.Index});
                T[closest].Helper=Vi;
                T.push_back(ei);
                break;

            case MERGE:

                for (int i=0; i<(int)T.size(); i++){
                    if (T[i].Index == (int)(Vi.Index+1)%(int)Points.size()){
                        if (T[i].Helper.Type==MERGE){
                            New_Edges.push_back({Vi.Index,T[i].Helper.Index});
                        }
                        T.erase(T.begin() + i);
                        break;
                    }
                }
                closest = find_left_intersect(T, Vi);
                
                if (T[closest].Helper.Type==MERGE){
                    New_Edges.push_back({Vi.Index,T[closest].Helper.Index});
                }
                T[closest].Helper = Vi;

                break;
            case REGULAR:

                if (Vi.Point.y>Vi.Next_Point.y){

                    for (int i=0; i<(int)T.size(); i++){
                        if (T[i].Index == (int)(Vi.Index+1)%(int)Points.size()){
                            if (T[i].Helper.Type==MERGE){
                                New_Edges.push_back({Vi.Index,T[i].Helper.Index});
                            }
                            T.erase(T.begin() + i);
                            break;
                        }
                    }

                    T.push_back(ei);

                } else {
                    closest = find_left_intersect(T, Vi);
                    if (T[closest].Helper.Type==MERGE){
                        New_Edges.push_back({Vi.Index,T[closest].Helper.Index});
                    }
                    T[closest].Helper = Vi;
                }
                break;
        }
        Q.pop();
    }

    return New_Edges;

}

vector<MonoPoint> Sort_Points(vector<MonoPoint> Points){
    int count =0;
    vector<MonoPoint> Sorted_Points = Points;
    for (int i=0; i<(int)Sorted_Points.size()-1; i++){
        for (int j=i+1; j<(int)Sorted_Points.size(); j++){
            if (Sorted_Points[i].Point.y>Sorted_Points[j].Point.y){
                count++;
                MonoPoint temp = Sorted_Points[i];
                Sorted_Points[i] = Sorted_Points[j];
                Sorted_Points[j] = temp;
            }
        }
    }
    cout << count << endl;
    return Sorted_Points;
}

vector<array<Vector2,3>> Mono_Triangulate(vector<MonoPoint> Sorted_Points){

    vector<MonoPoint> Points = Sorted_Points;

    vector<array<Vector2,3>> Triangles;

    vector<MonoPoint> Stack;

    Stack.push_back(Points[0]);
    Stack.push_back(Points[1]);

    for (int i=2; i<(int)Points.size()-1; i++){
        if (Points[i].Side!=Stack.back().Side){
            MonoPoint previous = Stack.back();
            Stack.pop_back();
            while (Stack.size()>0){
                Triangles.push_back({Points[i].Point,previous.Point,Stack.back().Point});
                previous = Stack.back();
                Stack.pop_back();
            }
            Stack.push_back(Points[i-1]);
            Stack.push_back(Points[i]);



        } else {
            while (true){
                MonoPoint popped = Stack.back();
                Stack.pop_back();

                Vector2 p = Points[i].Point;
                Vector2 q = popped.Point;
                Vector2 r = Stack.back().Point;
                if (((((q.x-p.x)*(r.y-p.y)) - ((r.x-p.x)*(q.y-p.y)) > 0 && Points[i].Side==LEFT) || (((q.x-p.x)*(r.y-p.y)) - ((r.x-p.x)*(q.y-p.y)) < 0 && Points[i].Side==RIGHT)) && Stack.size()>0){
                    Triangles.push_back({p,q,r});

                } else {
                    Stack.push_back(popped);
                    Stack.push_back(Points[i]);
                    break;
                }
            }
        }
    }

    MonoPoint popped = Stack.back();
    Stack.pop_back();
    while (Stack.size()>0){
        Triangles.push_back({Points.back().Point,popped.Point,Stack.back().Point});
        popped = Stack.back();
        Stack.pop_back();
    }
    return Triangles;
}

vector<vector<MonoPoint>> Create_Mono(vector<Vector2> Points, vector<array<int,2>> New_Edges){

    vector<priority_queue<MonoPoint, vector<MonoPoint>, CompareMonoY>> Monotone_Queue;

    vector<array<int,2>> start_ends = {{0,(int)Points.size()-1}};

    for (array<int,2> Edge: New_Edges){
        start_ends.push_back({min(Edge[0],Edge[1]),max(Edge[0],Edge[1])});
    }
    
    for (array<int,2> se_pair: start_ends){
        bool end = false;

        Monotone_Queue.push_back({});

        int i = se_pair[0];

        while (!end){
            vector<int> paths = {(i+1)%(int)Points.size()};
            
            if (i==(int)Points.size()-1 && se_pair[0]==0){
                end = true;
            }
            for (array<int,2> Edge: New_Edges){
                if (i==min(Edge[0],Edge[1]) && !(i==se_pair[0] && se_pair[1]==max(Edge[0],Edge[1]))){
                    paths.push_back(max(Edge[0],Edge[1]));
                } else if (i==max(Edge[0],Edge[1]) && i==se_pair[1] && se_pair[0]==min(Edge[0],Edge[1])){
                    paths.push_back(min(Edge[0],Edge[1]));
                    end = true;
                }
            }


            int next=0;
            if (end){
                next=se_pair[0];
            } else {
                for (int path: paths){
                    if (path>next and path<=se_pair[1]){
                        next=path;
                    }
                }
            }
            if (Points[i].y<Points[next].y){
                Monotone_Queue.back().push({Points[i],RIGHT});
            } else {
                Monotone_Queue.back().push({Points[i],LEFT});
            }
            i = next;
        }
    }

    vector<vector<MonoPoint>> Monotone_Points;

    for (priority_queue<MonoPoint, vector<MonoPoint>, CompareMonoY> Queue: Monotone_Queue){
        Monotone_Points.push_back({});
        while (!Queue.empty()){
            Monotone_Points.back().push_back(Queue.top());
            Queue.pop();
        }
    }

    return Monotone_Points;
}

vector<array<Vector2,3>> Forwards_Triangulate(vector<Vector2> Points){

    vector<array<int,2>> New_Edges = Add_Edges(Points);

    vector<vector<MonoPoint>> MPoints = Create_Mono(Points,New_Edges);

    vector<array<Vector2,3>> Triangles;

    for (int i=0; i<(int)MPoints.size(); i++){
        vector<array<Vector2,3>> new_triangles = Mono_Triangulate(MPoints[i]);
        for (int j=0; j<(int)new_triangles.size(); j++){
            Triangles.push_back(new_triangles[j]);
        }
    }
    return Triangles;


}

vector<array<Vector2,3>> Reverse_Triangulate(vector<Vector2> Points){
    vector<Vector2> New_Points = Points;
    for(int i=0;i<(int)New_Points.size(); i++){
        New_Points[i].y*=-1;
    };

    vector<array<Vector2,3>> Triangles = Forwards_Triangulate(New_Points);

    vector<array<Vector2,3>> New_Triangles = Triangles;
    for(int i=0;i<(int)New_Triangles.size(); i++){
        New_Triangles[i][0].y*=-1;
        New_Triangles[i][1].y*=-1;
        New_Triangles[i][2].y*=-1;
    };
    return New_Triangles;
}

bool is_clockwise(vector<Vector2> Points){
    float total=0;
    for (int i=0; i<(int)Points.size(); i++){
        total += (Points[i+1].x - Points[i].x)*(Points[i+1].y + Points[i].y);
    }
    total += (Points.front().x - Points.back().x)*(Points.front().y + Points.back().y);

    return total<0;

}

vector<array<Vector2,3>> Triangulate(vector<Vector2> Points){
    vector<array<Vector2,3>> Triangles;

    if (is_clockwise(Points)){
        Triangles = Forwards_Triangulate(Points);
    } else {
        Triangles = Reverse_Triangulate(Points);
    }
    return Triangles;

}


int main() 
{
    srand(time(0));
    constexpr int screenWidth = 1420;
    constexpr int screenHeight = 780;

    int n = 20;

    vector<Vector2> Points;

    for (int i=0; i<2*n; i++){
        int r = 200+(rand() % 100);
        float x = screenWidth/2 - 2*r*cos(2+PI*i/n);
        float y = screenHeight/2 + r*sin(2+PI*i/n);
        Points.push_back(Vector2{x,y});
    }

    vector<array<Vector2,3>> Triangles;

    InitWindow(screenWidth, screenHeight, "My first RAYLIB program!");
    SetTargetFPS(60);
    

    while (!WindowShouldClose())
    {
        BeginDrawing();
            ClearBackground(BLACK);
            Triangles = Triangulate(Points);
            for (array<Vector2,3> triangle : Triangles){
                DrawTriangle(triangle[0],triangle[1],triangle[2],RED);
                DrawTriangle(triangle[2],triangle[1],triangle[0],RED);
                // DrawLineV(triangle[0],triangle[1],GRAY);
                // DrawLineV(triangle[1],triangle[2],GRAY);
                // DrawLineV(triangle[2],triangle[0],GRAY);
            }
            DrawFPS(50,50);
        EndDrawing();
    }
    CloseWindow();
}