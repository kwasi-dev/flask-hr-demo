from app.models.employee import Employee
from . import employee as e
from . import department as d
from . import user as u
from . import disciplinary_action as da
from . import appraisal as a
from . import swipe_card as sc
from . import employee_swipe_card as esc
from . import leave_type as lt
from . import leave_approval as la
from . import timesheet as t

# Simplifying names here so that the importation in other parts of the app is more readable
Employee = e.Employee
Department = d.Department
User = u.User
DisciplinaryAction = da.DisciplinaryAction
Appraisal = a.Appraisal
SwipeCard = sc.SwipeCard
EmployeeSwipeCard = esc.EmployeeSwipeCard
LeaveType = lt.LeaveType
LeaveApproval = la.LeaveApproval
Timesheet = t.Timesheet