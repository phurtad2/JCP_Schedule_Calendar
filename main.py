import jcp_weekly

print("JCP SCHEDULE TO GOOGLE CALENDAR\n"
      "----------------------------------\n"
      "(Please make sure your username and password are correct before proceeding(not yet implemented)\n"
      "(Future Plans: Make it work for any username/password, and input it to a given calendarID)\n"
      "Running...\n")
print('How many weeks would you like to input? (usually 2-3 is a good number for JCP)')
n = input()
jcp_weekly.set_work_cal(n)
print("Complete! Work Schedule is now on Work Calendar.")


