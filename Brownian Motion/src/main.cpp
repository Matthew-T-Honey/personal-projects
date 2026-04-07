#include <raylib.h>
#include <iostream>
#include <array>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <tgmath.h>
#include <vector>
#include <raymath.h>

using namespace std;

const int n = 300;
const float G = 0.01f;
const unsigned int segments = 360;



class Ball 
{
    private:
        Vector2 pos;
        Vector2 speed;
        double radius;
        double mass;
        int index;
        bool stuck;

        void Reset(){
            mass = 100.0f; //1.0f/pow(static_cast<float>(rand())/static_cast<float>(RAND_MAX),0.25) - 1.0f;

            radius = max(sqrt(mass),1.0);

            pos = { static_cast<float>(radius + rand() % (GetScreenWidth() - 2 * (int)radius)),
                    static_cast<float>(radius + rand() % (GetScreenHeight() - 2 * (int)radius))};

            speed = {   0.0f * static_cast<float>(rand()-RAND_MAX/2)/static_cast<float>(RAND_MAX),
                        0.0f * static_cast<float>(rand()-RAND_MAX/2)/static_cast<float>(RAND_MAX)};

            //speed.x -= 0.0002 * (pos.y-GetScreenHeight()/2) / sqrt(Vector2Distance(pos, (Vector2){GetScreenWidth()/2,GetScreenHeight()/2}));
            //speed.y += 0.0002 * (pos.x-GetScreenWidth()/2)  / sqrt(Vector2Distance(pos, (Vector2){GetScreenWidth()/2,GetScreenHeight()/2}));
        }

    public:
        Ball(int i)
        {
            Reset();
            index  = i;
            stuck = false;

        }

        Ball(Vector2 p, Vector2 s, double r, double m, int i)
        {
            pos = p;
            speed = s;
            radius = r;
            mass = m;
            index  = i;
            stuck = false;
        }

        void UpdatePos() 
        {   
            pos = Vector2Add(pos, speed);
            
            const int screenWidth = GetScreenWidth();
            const int screenHeight = GetScreenHeight();
            
            if(pos.x + radius >= screenWidth || pos.x - radius <= 0)
            {
                speed.x *= -1;
            }

            if(pos.y + radius >= screenHeight || pos.y - radius <= 0)
            {
                speed.y *= -1;
            }  
            if(pos.x - radius >= screenWidth || pos.x + radius <= 0)
            {
                Reset();
            }

            if(pos.y - radius >= screenHeight || pos.y + radius <= 0)
            {
                Reset();
            }  
            }

        void UpdateSpeed(vector<Ball> &balls) 
        {
            bool still_stuck = false;

            const int screenWidth = GetScreenWidth();
            const int screenHeight = GetScreenHeight();

            for (int i=0; i<n; i++){
                if (i < index){

                    float dx = pos.x - balls[i].get_pos().x;
                    float dy = pos.y - balls[i].get_pos().y;
                    float distance = Vector2Distance(pos, balls[i].get_pos());
                    float accel = G * balls[i].get_mass()/pow(distance,3);
                    
                    if (balls[i].get_rad()+get_rad() > distance){

                        Vector2 v1 = speed;
                        Vector2 v2 = balls[i].get_speed();
                        Vector2 x1 = pos;
                        Vector2 x2 = balls[i].get_pos();


                        float angle = atan2(x1.y-x2.y,x1.x-x2.x);

                        
                        float deltav = cos(angle) * (v1.x-v2.x) + sin(angle) * (v1.y-v2.y);
                        
                        speed.x -= deltav*cos(angle);
                        speed.y -= deltav*sin(angle);

                        balls[i].set_speed(Vector2 {v2.x + deltav*cos(angle),v2.y + deltav*sin(angle)});

                        still_stuck = true;
                        if (stuck){
                            //Reset();
                            //cout << "Stuck On Ball\n";
                        }
                        stuck = true;
                    } 
                    speed = Vector2Subtract(speed,Vector2Scale((Vector2){dx,dy},accel));
                }
            }
            if (!still_stuck){
                stuck = false;
            }
            //speed.y += 0.005;
            speed = Vector2Scale(speed,0.999);
        }

        void Draw() const
        {
            float s = 100.0f*Vector2Length(speed);
            Color color = {min(static_cast<int>(s),255), max(255 - static_cast<int>(s),0), max(255 - static_cast<int>(s),0), 255};
            DrawCircle(pos.x, pos.y, radius, color);
        }

        Vector2 get_pos()
        {
            return pos;
        }
        Vector2 get_speed()
        {
            return speed;
        }

        void set_speed(Vector2 new_speed)
        {
            speed = new_speed;
        }

        double get_rad()
        {
            return radius;
        }

        double get_mass()
        {
            return mass;
        }
        
        void put_data(Vector2 p, Vector2 s, double r)
        {
            pos = p;
            speed = s;
            radius = r;
        }

        void merge(Vector2 s, double m)
        {
            speed.x = (speed.x*mass + s.x*m) / (m+mass);
            speed.y = (speed.y*mass + s.y*m) / (m+mass);
            mass = min(mass + m, 100.0);
            radius = max(sqrt(mass),1.0);
        }

        void Draw_Orbit(vector<Ball> &balls)
        {
            float largest = 0;
            int index = 0;
            for (int i=0; i<n; i++){
                float distance = Vector2Distance(pos, balls[i].get_pos());

                if (balls[i].get_mass()/pow(distance,2) > largest && !Vector2Equals(pos,balls[i].get_pos()) ){
                    largest = balls[i].get_mass()/pow(distance,2);
                    index = i;
                } 
            }
            
            if (largest>0.00000005){
  

                float x = pos.x - balls[index].get_pos().x;
                float y = pos.y - balls[index].get_pos().y;

                float v = Vector2Length(Vector2Subtract(speed,balls[index].get_speed()));
                float d = Vector2Distance(pos, balls[index].get_pos());

                float u = G*balls[index].get_mass();
                
                float a = (u*d)/(2*u-d*v*v);

                float vt = (x*speed.y - y*speed.x)/d;

                float vr = (x*speed.x + y*speed.y)/d;

                float e = sqrt(1 + ((d * vt*vt)/u) * (d * v*v / u -2));

                if (e<1){

                    float theta = copysign(1.0, vt*vr) * acos( ((a*(1-e*e)) - d) / (e* d)) - atan2(y,x);

                    array<float,segments> Angles;
                    for (int i=0; i < segments; i++){
                        Angles[i] = i * 2 * PI / segments;
                    }
                    array<float,segments> Radii;
                    for (int i=0; i < segments; i++){
                        Radii[i] = a*(1-e*e)/(1+e*cos(Angles[i] + theta));
                    }

                    Vector2 points[segments+1];
                    for (int i=0; i < segments+1U; i++){
                        points[i].x = balls[index].get_pos().x + Radii[i%segments] * cos(Angles[i%segments]);
                        points[i].y = balls[index].get_pos().y + Radii[i%segments] * sin(Angles[i%segments]);
                    }

                    DrawLineStrip(points, segments+1, WHITE);
                }
            }
        }
};



int main() 
{
    srand(time(nullptr));
    const Color Background = {0, 0, 0, 255};


    InitWindow(0, 0, "My first RAYLIB program!");

    ToggleBorderlessWindowed();  

    int screenWidth = GetScreenWidth();
    int screenHeight = GetScreenHeight();

    vector<Ball> balls;

    Ball Planet({static_cast<float>(screenWidth)/2,static_cast<float>(screenHeight)/2},{0.0,0.0},10,100,n);
    

    for (int i=0; i<n; i++){
        Ball ball(i);
        balls.push_back(ball);
    };
    //balls.push_back(Planet);

    //SetTargetFPS(300);

    int count = 0;
    
    while (!WindowShouldClose())
    {   
        for (int i=0; i<n; i++){
            balls[i].UpdateSpeed(balls);
        };
        for (int i=0; i<n; i++){
            balls[i].UpdatePos();
        };
        
            
        BeginDrawing();
            ClearBackground(Background);
            
            for (int i=0; i<n; i++){
                if (balls[i].get_mass()>0){
                    //balls[i].Draw_Orbit(balls);
                }
            };
            for (int i=0; i<n; i++){
                balls[i].Draw();
            };
        EndDrawing();

        float KE = 0;

        for (int i=0; i<n; i++){
                KE += 0.5 * balls[i].get_mass() * pow(Vector2Length(balls[i].get_speed()),2);
            };

        if (count == 100){
            cout << "FPS = " << GetFPS() << ", KE = " << KE << "\n";
            count = 0;
        }

        count++;
        

    };
    
    CloseWindow();
}