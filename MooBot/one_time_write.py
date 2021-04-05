from moodle_scrapper import *

STUDENT_ID = "YOUR_STUDENT_ID"
LOGIN_PASSWORD = "YOUR_LOGIN_PASSWORD"

if __name__ == "__main__":
  #logging in
  print("logging in...")
  session = login(STUDENT_ID, LOGIN_PASSWORD)

  #get courses
  print("getting Courses...")
  course_dict = getCourses(session)
  print(course_dict)

  write_old_forum_posts(course_dict,session)
  write_old_activities(course_dict,session)