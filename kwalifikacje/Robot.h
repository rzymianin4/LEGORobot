#ifndef Robot_h
#define Robot_h

#include <vector>
#include "instrumental_package.h"

class Robot {
	private:
		void system_move(double);
		void system_turn(angle);
		void make_step(bool);
		bool scan_pp(colour, int, std::vector<std::pair<colour, int> >&);
		colour scan_colour();

	protected:
		std::pair<double, double> position;
		angle direction;
		const double robot_lenth;
		const double step;
		const angle turn_step;
		const angle step_dev;
		const double step_noise;
		const angle turn_noise;
		double drive_time;

		void align();

	public:
		double speed;
		double turn_speed;

		Robot(double input[8]): position(std::make_pair(input[0], input[1])), robot_lenth(11), step(0.01*2*robot_lenth), turn_step(0.002), direction(input[2]), turn_noise(input[3]), step_noise(input[4]), step_dev(input[5]), speed(input[6]*22), turn_speed(input[7]) { }
		std::pair<double, double> get_position() { return position; }
		angle get_direction() { return direction; }
		std::vector<std::pair<colour, int> > move(colour, int);
		colour move(std::pair<double, double>);
		void move(double);
		void turn(angle);
		void beep();
		void end();
	};

#endif