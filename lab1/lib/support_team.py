from lib.robot import Robot


class SupportTeam:
    @staticmethod
    def fix_problem(robot: Robot) -> None:
        print("-"*60, "\nSupport team arrived")
        details = [robot.battery, robot.software, robot.mechanism]
        print("Searching for problem")
        for detail in details:
            if not detail.check_condition():
                print("Problem was with", str(detail))
                detail.fix_condition()
                print("Problem fixed")
        print("-"*60)
