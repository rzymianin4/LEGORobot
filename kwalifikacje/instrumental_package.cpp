#ifndef instrumental_package_cpp
#define instrumental_package_cpp

#include <cmath>
#include "instrumental_package.h"

void angle::calibrate() {
	if(value >= PI) {
		value-=(2*PI);
		calibrate(); }
	if(value < -PI) { 
		value+=(2*PI);
		calibrate(); } }

std::ostream& operator<< (std::ostream& out, const angle& theta){
	out << theta.value/PI << "*PI";
	return out; }

Field::Field(std::pair<double, double> number, colour col): col(col) {
	for(int i=1; i<=5; i++)
		if(number.first<12*i+2) {
			nr.first = i;
			break; }
	for(int i=1; i<=5; i++)
		if(number.second<12*i+2) {
			nr.second = i;
			break; } }

double count_distance(std::pair<double, double> point1, std::pair<double, double> point2) {
	return sqrt( pow(point2.first - point1.first, 2) + pow(point2.second - point1.second, 2) ); }

angle count_angle(std::pair<double, double> point1, std::pair<double, double> point2) {
	double del_x = point2.first-point1.first;
	double del_y = point2.second-point1.second;
	if(del_x) { 
		if(del_x>0) { return atan(del_y/del_x); }
		if(del_x<0) { return atan(del_y/del_x) + PI; } }	
	else if(del_y>0) { return PI/2; }
	else if(del_y<0) { return -PI/2; }
	return 0; }

#endif