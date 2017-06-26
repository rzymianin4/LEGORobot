#ifndef Controler_h
#define Controler_h

#include <vector>
#include "Robot.h"
#include "instrumental_package.h"

class Controler {
	private:
		double cpu_time;
		Field board[5][5];
		Robot* robot;
		std::vector<Field> red_vector;
		std::vector<Field> green_vector;
		std::vector<Field> blue_vector;

		double move_time(double);
		double turn_time(angle);
		void scan_pp(const std::vector<std::pair<colour, int> >&);
		std::vector<std::pair<colour, int> > sequence(bool);
		std::vector<Field> road_maker();

	public:
		Controler(double robot_in[8], double input): robot(), cpu_time(input) { robot = new Robot(robot_in); }
		void scan_map();
		void beep_tour();
};

#endif