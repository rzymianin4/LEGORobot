#include <map>
#include <string>
#include <sstream>
#include "instrumental_package.h"
#include "Robot.h"
#include "Controler.h"

using namespace std;

int main() {
	map<string, double> xmap = {
		{"x",0},
		{"y",1},
		{"angle",2},
		{"steering_noise",3},
		{"distance_noise",4},
		{"forward_steering_drift",5},
		{"speed",6},
		{"turning_speed",7},
		{"M",8},
		{"N",9},
		{"execution_cpu_time_limit", 10} };

	string s1,key;
	double robot_argument[8];
	double s2,control_argument;
	int j;

	for(int i =0;i<11;i++){
			getline(cin,s1);
			s1.replace(s1.find(":"),1," ");
			stringstream ss(s1);
			ss>>key>>s2;
			xmap[key] = s2; }
	
	robot_argument[0] = (xmap["x"] - 2)*22 +1;
	robot_argument[1] = (xmap["y"] - 2)*22 +1;
	robot_argument[2] = xmap["angle"];
	robot_argument[3] = xmap["steering_noise"];
	robot_argument[4] = xmap["distance_noise"];
	robot_argument[5] = xmap["forward_steering_drift"];
	robot_argument[6] = xmap["speed"];
	robot_argument[7] = xmap["turning_speed"];
	control_argument = xmap["execution_cpu_time_limit"];
	
	Controler controler(robot_argument, control_argument);
	controler.scan_map();
	controler.beep_tour();
	
return 0;
}