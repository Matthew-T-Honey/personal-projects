#include <raylib.h>
#include <iostream>
#include <raymath.h>
#include <array>
#include <string> 
#include <cmath>

using std::string;
using std::cout;
using std::max;
using std::array;

constexpr int screenWidth = 1920;
constexpr int screenHeight = 1080;
constexpr float CameraSpeed = 10.0;
constexpr int segments = 60;
constexpr float G = 0.1;
constexpr int n = 500;

float RandomUniform(void){
    return static_cast<float>(rand())/static_cast<float>(RAND_MAX);
};

class Islet;

class MapCamera{
    public:
        Vector2 position;
        float zoom;

        bool dragging = false;
        Vector2 dragging_from;

        bool tracking = false;
        int tracked = 0;

        MapCamera(Vector2 p = {0,0}, float z = 1.0){
            position = p;
            zoom = z;
        }

        void Update(){

            if (IsKeyDown(87)) {position.y-=CameraSpeed/zoom; tracking = false;}
            if (IsKeyDown(265)) {position.y-=CameraSpeed/zoom; tracking = false;}
            if (IsKeyDown(83)) {position.y+=CameraSpeed/zoom; tracking = false;}
            if (IsKeyDown(264)) {position.y+=CameraSpeed/zoom; tracking = false;}
            if (IsKeyDown(65)) {position.x-=CameraSpeed/zoom; tracking = false;}
            if (IsKeyDown(263)) {position.x-=CameraSpeed/zoom; tracking = false;}
            if (IsKeyDown(68)) {position.x+=CameraSpeed/zoom; tracking = false;}
            if (IsKeyDown(262)) {position.x+=CameraSpeed/zoom; tracking = false;}

            Vector2 mouse_pos = GetMousePosition();
            int scroll = GetMouseWheelMove();
            zoom *= pow(1.1,scroll);

            Vector2 local_mouse = Vector2Subtract(mouse_pos,Vector2{screenWidth/2,screenHeight/2});

            position= Vector2Add(position,Vector2Scale(local_mouse,(pow(1.1,scroll)-1)/zoom));  
            
            if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {dragging = true; dragging_from = mouse_pos;}

            if (IsMouseButtonReleased(MOUSE_BUTTON_LEFT)) dragging = false;
            if (dragging){
                position =  Vector2Subtract(position,Vector2Scale(Vector2Subtract(mouse_pos,dragging_from),1/zoom));
                dragging_from = mouse_pos;
            }
        }


        Vector2 Get_Relative_Position(Vector2 point){
            return Vector2Subtract(Vector2Scale(point,zoom),Vector2Subtract(Vector2Scale(position,zoom),Vector2{screenWidth/2,screenHeight/2}));
        }
};


float Solve_Kepler(float M, float e){

    float E = M;
    for (int i=0; i < 100; i++){
        E= E - (E-e*sin(E)-M)/(1-e*cos(E));
    }

    return E;

};

class Islet{
    public:
        float size;

        float e;

        float distance;

        float rotation;

        float period;

        float offset;

        Vector2 position;
        Islet(float s = 1.0){
            size = 1.0+5.0*RandomUniform()*RandomUniform();
            distance = 20+1000*pow(RandomUniform(),size/5.0);
            e = 0.1*RandomUniform();
            rotation = 2*PI*RandomUniform();
            period = G*sqrt(pow(distance/(1-e*e),3));
            offset = 10000*RandomUniform();
        }

        void Draw(MapCamera camera, float time){

            float n = 2*PI/period;
            float M = n*(time+offset);
            float E = Solve_Kepler(M,e);

            float theta =2*atan(tan(E/2)*sqrt((1+e)/(1-e)));

            float r = distance/(1+e*cos(theta));

            position.x = r * cos(theta);
            position.y = r * sin(theta);

            position = Vector2Rotate(position,rotation);

            DrawCircleV(camera.Get_Relative_Position(position),size*camera.zoom,WHITE);

            DrawCircleLinesV(camera.Get_Relative_Position(position),15.0*camera.zoom,BLUE);


        }

        void Draw_Orbit(MapCamera camera){
            array<float,segments> Angles;
            for (int i=0; i < segments; i++){
                Angles[i] = i * 2 * PI / segments;
            }

            array<float,segments> Radii;
            for (int i=0; i < segments; i++){
                Radii[i] = distance/(1+e*cos(Angles[i]));
            }

            Vector2 points[segments+3];
            for (int i=-2; i < segments+3; i++){
                points[i].x = Radii[i%segments] * cos(Angles[i%segments]);
                points[i].y = Radii[i%segments] * sin(Angles[i%segments]);
                points[i] = Vector2Rotate(points[i],rotation);
                points[i] = camera.Get_Relative_Position(points[i]);
            }

            DrawSplineCatmullRom(points, segments+3, 1,GRAY);

        }



};



int main() 
{

    InitWindow(screenWidth, screenHeight, "My first RAYLIB program!");
    SetTargetFPS(60);

    MapCamera camera = MapCamera(Vector2{0,0},0.5);

    Islet Zenith = Islet(10.0);

    float time=0;



    array<Islet,n> Islets{};

    for (int i=0; i<n; i++){
        Islets[i] = Islet();
    };

    
    Zenith.distance=0.01;
    Zenith.e=0.0;
    Zenith.rotation = 0;
    Zenith.period = 0.1;
    Zenith.size = 10.0;


    while (!WindowShouldClose())
    {


        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)){
            Vector2 mouse_pos = GetMousePosition();
            camera.tracking = false;
            for (int i=0; i<n; i++){
                if (CheckCollisionPointCircle(mouse_pos, camera.Get_Relative_Position(Islets[i].position), 10.0*camera.zoom)){
                    camera.tracking = true;
                    camera.tracked = i;
                }
            };
        }
        if (camera.tracking){
            camera.position = Islets[camera.tracked].position;
        }
        
        camera.Update();
        BeginDrawing();
            ClearBackground(BLACK);
            Zenith.Draw(camera,1.0);
            for (int i=0; i<n; i++){
                //Islets[i].Draw_Orbit(camera);
            };
            for (int i=0; i<n; i++){
                Islets[i].Draw(camera,time);
            };
        EndDrawing();
        time++;


    }
    
    CloseWindow();
}