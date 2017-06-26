#ifndef Robot_cpp
#define Robot_cpp

#include <cmath>
#include <string>
#include <sstream>
#include "Robot.h"

void Robot::make_step(bool B) {
	int sense = pow(-1, B);
	std::cout << "MOVE" << ' ' << sense << std::endl;
	position.first += (sense*step*cos(direction));
	position.second += (sense*step*sin(direction));
	direction += 2*sense*step_dev; }

void Robot::system_move(double distance) {
	double n_step = distance / step;
	std::cout << "MOVE " << round(n_step) << std::endl;
	scan_colour(); }

void Robot::system_turn(angle value) {
	double n_step = value / turn_step;
	std::cout << "TURN " << round(-n_step) << std::endl;
	scan_colour(); }

bool Robot::scan_pp(colour req_col, int number, std::vector<std::pair<colour, int> >& past_path) {
	int i = 0;
	for(auto iterator : past_path) {
		if(iterator.first == req_col) { i++; } }
	if(i<number) { return true; }
	else { return false; } }

colour Robot::scan_colour() { 
	std::string command;
	int R,G,B;
	bool colour_loaded;
	while(1) {
		std::cin >> command;
		if(command == "time") {
			std::cin>>drive_time;}
		else if(command == "color") {
			std::cin >> R >> G >> B;
			colour_loaded = 1; }
		else if(command ==  "act") { break; } }
	if(!colour_loaded) { return col_err; }
	if(R>G+B) { return red; }
	else if(G>R+B) { return green; }
	else if(B>G+R) { return blue; }
	else if(R<100 && G<100 && B<100) { return black;  }
	else { return white; } }


void Robot::align() {
	angle bound = 0;
	if(direction >= PI/2 || direction < -PI/2) { bound = PI; }
	turn(bound-direction); }


std::vector<std::pair<colour, int> > Robot::move(colour req_col, int number) {
	std::vector<std::pair<colour, int> > past_path;
	colour curr_col;
	do {
		make_step(0);
		curr_col = scan_colour();
		if(past_path.size()) {
			if(past_path.back().first != curr_col && past_path.back().first != col_err) {
				past_path.emplace_back(curr_col, 0);
				if(!curr_col) { align();} } }
		else{ past_path.emplace_back(curr_col, 0); }
		past_path.back().second +=1;
	}while(scan_pp(req_col, number, past_path));
	return past_path; }

colour Robot::move(std::pair<double, double> target) {
	colour col;
	double distance = count_distance(position, target);
	angle aim = count_angle(position, target);
	angle aim_dev = acos(1-(distance*distance*step_dev*step_dev)/(2*step*step));
	distance = abs(aim_dev*step/step_dev);
	aim_dev *= step_dev>0?-0.5:0.5;
	turn(aim-direction+aim_dev);	
	if(distance<robot_lenth) {
		make_step(0);
		col = scan_colour();
		move(distance); }
	else {
		move(distance-robot_lenth);
		make_step(0);
		col = scan_colour();
		move(robot_lenth); }
	return col; }

void Robot::move(double distance) {
	distance = round(distance / step)*step;
	system_move(distance);
	direction += step_dev*(distance/step)/2;
	position.first += distance*cos(direction);
	position.second += distance*sin(direction);
	direction += step_dev*(distance/step)/2; }

void Robot::turn(angle value) {
	value= round(value / turn_step)*turn_step;
	system_turn(value);
	direction+=value; }

void Robot::beep() {
	std::cout << "BEEP" << std::endl; 
	scan_colour();}  

void Robot::end() {
	std::cout << "FINISH" << std::endl;
	scan_colour(); }

#endif