import datetime

daysstr = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
#Last day of class 12/4
#Final Examples 12/9-14
FIRSTDAY = datetime.date(2025, 1, 22)
Ds = [datetime.timedelta(2), datetime.timedelta(3), datetime.timedelta(2)]  #Wednesday To Friday, Friday To Monday, Monday To Wednesday
Holidays = {datetime.date(2025, 3, 10):"Spring Break", datetime.date(2025, 3, 12):"Spring Break", datetime.date(2025, 3, 14):"Spring Break", datetime.date(2025, 4, 23):"COSA Day"}

schedule_HTML = ""

#Load in assignments first, which will be peppered throughout the syllabus
fin = open("syllabus_content_assignments.txt", "r")
lines = fin.readlines()
fin.close()
assignments = []
for i in range(int(len(lines)/3)):
    datefields = [int(s) for s in str.split(lines[i*3+2], '-')]
    date = datetime.date(datefields[0], datefields[1], datefields[2])
    assignments.append([date, lines[i*3], lines[i*3+1]])

#Parse syllabus info and order by date
fin = open("syllabus_content_lectures.txt", "r")
lines = fin.readlines()
date = FIRSTDAY
addidx = 0
coloridx = 0
colors = ["#f9fafb", "#ffffff"]
assignment_color = "#f4e6e7"
use_colors = False
lecnum = 1

for i in range(int(len(lines)/4)):
    L = [l.rstrip() for l in lines[i*4:(i+1)*4]]
    if L[0] == "SECTION":
        schedule_HTML += "<tr><td colspan = \"5\"><h2><b>%s</b></h2><p>%s</p></td></tr>\n"%(L[1], L[2])
    elif L[0] == "LECTURE":
        #Handle holidays
        while date in Holidays:
            color = colors[coloridx]
            coloridx = (coloridx + 1)%2
            day = daysstr[date.weekday()%7]
            taskstr = "No CS 372 Class.  Enjoy the break!"
            if "Designated" in Holidays[date]:
                taskstr = "No CS 372 Class"
            schedule_HTML += "<tr><td>--</td><td>%s %i/%i/%i</td><td>%s</td><td></td><td>%s</td></tr>\n"%(day, date.month, date.day, date.year, Holidays[date], taskstr)
            date = date + Ds[addidx]
            addidx = (addidx + 1)%len(Ds)
        #Ordinary lectures
        color = colors[coloridx]
        coloridx = (coloridx + 1)%2
        day = daysstr[date.weekday()%7]
        assignmentsDueToday = []
        for a in assignments:
            if a[0] == date:
                assignmentsDueToday.append(a)
        if use_colors:
            schedule_HTML += "<tr bgcolor = %s>"%color
        else:
            schedule_HTML += "<tr>"
        schedule_HTML += "<td>%i</td>"%lecnum 
        schedule_HTML += "<td>%s %i/%i/%i</td>"%(day, date.month, date.day, date.year)
        if len(L[2]) > 0:
            schedule_HTML += "<td><a href = \"../Lectures/%s\">%s</a></td>"%(L[2], L[1])
        else:
            schedule_HTML += "<td>%s</td>"%L[1]
        schedule_HTML += "<td>%s</td>"%L[3]
        if len(assignmentsDueToday) > 0:
            schedule_HTML += "<td bgcolor=%s>"%assignment_color
        else:
            schedule_HTML += "<td>"
        for a in assignmentsDueToday:
            if len(a[2].strip()) > 0:   
                schedule_HTML += "<a href = \"%s\">%s</a>"%(a[2], a[1])
            else:
                schedule_HTML += "%s"%a[1]
        schedule_HTML += "</td></tr>\n"
        nextdate = date + Ds[addidx]
        addidx = (addidx + 1)%len(Ds)
        #Check to see if any assignments are in between this date and the next date
        assignmentsDueInBetween = []
        for a in assignments:
            if (a[0] - date).days > 0 and (nextdate - a[0]).days > 0:
                assignmentsDueInBetween.append(a)
        if len(assignmentsDueInBetween) > 0:
            for a in assignmentsDueInBetween:
                if use_colors:
                    schedule_HTML += "<tr bgcolor = %s>"%assignment_color
                else:
                    schedule_HTML += "<tr>"
                schedule_HTML += "<td></td><td>%s %i/%i/%i</td><td></td><td></td><td bgcolor=%s>"%(daysstr[a[0].weekday()], a[0].month, a[0].day, a[0].year, assignment_color)
                if len(a[2].strip()) > 0:
                    schedule_HTML += "<a href = \"%s\">%s</a>"%(a[2], a[1])
                else:
                    schedule_HTML += "%s"%a[1]
                schedule_HTML += "</td></tr>"
        date = nextdate
        lecnum += 1
fin.close()

fin = open("index.html")
lines = fin.readlines()
fin.close()


# Put schedule into index.html
BEFORE_SCHEDULE = 0
IN_SCHEDULE = 1
AFTER_SCHEDULE = 2

state = BEFORE_SCHEDULE
fout = open("index.html", "w")
for line in lines:
    if state == BEFORE_SCHEDULE:
        fout.write(line)
        if "<!-- Begin Schedule -->" in line:
            state = IN_SCHEDULE
            fout.write(schedule_HTML)
    elif state == IN_SCHEDULE:
        if "<!-- End Schedule -->" in line:
            fout.write(line)
            state = AFTER_SCHEDULE
    else:
        fout.write(line)
fout.close()




filename = "index.html"
fin = open(filename)
lines = fin.readlines()
fin.close()
fin = open(filename, 'w')
in_updated = 0
for line in lines:
    if line.find("<!-- Start of Last Updated -->") != -1:
        in_updated = 1
        continue
    if line.find("<!-- End of Last Updated -->") != -1:
        in_updated = 0
        fin.write("<!-- Start of Last Updated -->\n")
        d = datetime.date.today()
        fin.write("<h2><b>Course Evolving: Site Last Updated %i/%i/%i\n</b></h2>"%(d.month, d.day, d.year))
        fin.write("<!-- End of Last Updated -->\n")
        continue
    if in_updated == 0:
        fin.write(line)
fin.close()
