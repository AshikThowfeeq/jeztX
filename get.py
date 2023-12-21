import os
import django



from myapp.models import EmployeeCameraAssignment

def list_all_cameras():
    # Fetch all unique cameras from EmployeeCameraAssignment
    camera_assignments = EmployeeCameraAssignment.objects.all()
    unique_camera_names = set()
    for assignment in camera_assignments:
        unique_camera_names.add(assignment.cam.cam_name)
    print(unique_camera_names)
    return list(unique_camera_names)

# list_all_cameras()



def list(camera_name):
    # Query for all assignments for the specified camera
    assignments = EmployeeCameraAssignment.objects.filter(cam__cam_name=camera_name)
    # Extract employee IDs from these assignments
    employee_ids = [assignment.employee.employee_id for assignment in assignments]

    print(employee_ids)
    return employee_ids

list("109d")