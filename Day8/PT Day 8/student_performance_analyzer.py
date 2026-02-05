import numpy as np
marks = np.array([
    [[78, 80, 82], [85, 87, 88], [90, 92, 94], [70, 72, 74]],
    [[68, 70, 72], [75, 77, 78], [80, 82, 84], [65, 67, 69]],
    [[88, 90, 92], [92, 94, 96], [85, 87, 89], [78, 80, 82]],
    [[58, 60, 62], [65, 67, 69], [70, 72, 74], [60, 62, 64]],
    [[82, 84, 86], [88, 90, 92], [91, 93, 95], [75, 77, 79]]
])
print("Marks Array Shape:", marks.shape)
student_avg = np.mean(marks, axis=(1, 2))
print("\nAverage marks of each student:")
print(student_avg)
subject_avg = np.mean(marks, axis=(0, 2))
print("\nAverage marks of each subject:")
print(subject_avg)
exam_avg = np.mean(marks, axis=(0, 1))
print("\nAverage marks of each exam:")
print(exam_avg)
topper = np.argmax(student_avg) + 1
print("\nTopper is Student:", topper)