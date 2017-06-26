#ifndef instrumental_package_h
#define instrumental_package_h

#include <iostream>

const double PI = 3.1415926536;


class angle {
	private:
		double value;
		void calibrate();
		
	public:
		angle(): value(0) { }
		angle(double number): value(number) { calibrate(); }
		angle(const angle& theta): value(theta.value) { }

		operator double () { return this->value; }
		operator double () const { return this->value; }
		angle& operator=(double number) {
			value = number;
			calibrate();
			return *this; }
		angle& operator+= (double number) {
			value+=number;
			calibrate();
			return *this; }
		angle& operator-= (double number) {
			value-=number;
			calibrate();
			return *this; }
		angle& operator*= (double number) {
			value*=number;
			calibrate();
			return *this; }
		angle& operator/= (double number) {
			value/=number;
			calibrate();
			return *this; }

		friend std::ostream& operator<< (std::ostream&, const angle&);
};

enum colour {
	col_err = -2,
	white = -1,
	black = 0,
	red = 1,
	green = 2,
	blue = 3
};

class Field {
	public:
		std::pair<int, int> nr;
		colour col;

		Field() { }
		Field(std::pair<int, int> number, colour col): nr(number), col(col) { }
		Field(std::pair<double, double> number, colour col);
		~Field() { }

		operator std::pair<double, double> () {
			return std::make_pair(12+nr.first*22.0, 12+nr.second*22.0); }
};

double count_distance(std::pair<double, double>, std::pair<double, double>);
angle count_angle(std::pair<double, double>, std::pair<double, double>);

#endif