#ifndef Controler_cpp
#define Controler_cpp

#include <cmath>
#include "Controler.h"

double Controler::move_time(double distance) {
	return distance/robot->speed; }

double Controler::turn_time(angle value) {
	return value/robot->turn_speed; }

void Controler::scan_pp(const std::vector<std::pair<colour, int> >& past_path) {
	static int record;
	int i = 0;
	for(auto iterator : past_path) {
		if(iterator.first) { board[i%2?5-i:i][record] = Field(std::make_pair(i, record), iterator.first); 
			if(iterator.first == red){ red_vector.push_back(board[i%2?5-i:i][record]); }
			else if(iterator.first == green) { green_vector.push_back(board[i%2?5-i:i][record]); }
			else if(iterator.first == blue) { blue_vector.push_back(board[i%2?5-i:i][record]); }
			i++; } }
	record++; }

std::vector<std::pair<colour, int> > Controler::sequence(bool rl) {
	std::vector<std::pair<colour, int> > past_path = robot->move(black, 5);
	robot->turn((rl?-1:1)*(PI/2-std::atan(6.0/22)));
	robot->move(sqrt(22*22+6*6));
	robot->turn((rl?-1:1)*(PI/2+std::atan(6.0/22)));
	return past_path; }

std::vector<Field> Controler::road_maker() {
	std::vector<Field> node;
	double best_time=240;
	double curr_time;
	for(auto it_R: red_vector) {
		for(auto it_G: green_vector) {
			for(auto it_B:blue_vector) {
				curr_time = move_time(count_distance(it_R, it_G) + count_distance(it_G, it_B)) + turn_time(count_angle(it_G, it_B));
				if(best_time > curr_time) {
					best_time = curr_time;
					Field array[3]= {it_R, it_G, it_B};
					node.assign(array, array+3); } } } } 
	return node; }
	

void Controler::scan_map() {
	robot->move(-3);
	for(int i=0; i<4; i++) { scan_pp(sequence(i%2)); }
	scan_pp(robot->move(black, 5)); }
	
void Controler::beep_tour() {
	std::vector<Field> node = road_maker();
	if(abs(robot->get_position().first-(22*node[0].nr.first+12))>8 && abs(robot->get_position().second-(22*node[0].nr.second+12))>8) {
		robot->move(node[0]); }
	robot->turn(count_angle(node[0], node[1])-robot->get_direction());
	robot->beep();
	for(int i=1; i<3; i++) {
		robot->move(node[i]);
		robot->beep(); }
	robot->end(); }

#endif