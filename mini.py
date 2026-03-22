import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')

fig.patch.set_facecolor('white')

# Head — large black circle
head = plt.Circle((5, 4.5), 3.2, color='black', zorder=1)
ax.add_patch(head)

# Ears — two smaller black circles
ear_left = plt.Circle((2.8, 7.2), 1.5, color='black', zorder=0)
ear_right = plt.Circle((7.2, 7.2), 1.5, color='black', zorder=0)
ax.add_patch(ear_left)
ax.add_patch(ear_right)

# Face / skin area — peach ellipse
face = patches.Ellipse((5, 4.2), 4.6, 4.0, color='#F5C9A0', zorder=2)
ax.add_patch(face)

# Eyes — white circles with black pupils
eye_left_white = plt.Circle((3.7, 5.4), 0.62, color='white', zorder=3)
eye_right_white = plt.Circle((6.3, 5.4), 0.62, color='white', zorder=3)
ax.add_patch(eye_left_white)
ax.add_patch(eye_right_white)

eye_left_pupil = plt.Circle((3.78, 5.42), 0.28, color='black', zorder=4)
eye_right_pupil = plt.Circle((6.38, 5.42), 0.28, color='black', zorder=4)
ax.add_patch(eye_left_pupil)
ax.add_patch(eye_right_pupil)

# Nose — small black ellipse
nose = patches.Ellipse((5, 4.3), 0.55, 0.38, color='black', zorder=3)
ax.add_patch(nose)

# Mouth — curved smiling arc drawn as a wedge outline (Arc)
mouth = patches.Arc((5, 3.6), 2.2, 1.4, angle=0,
                     theta1=200, theta2=340,
                     color='black', linewidth=3, zorder=3)
ax.add_patch(mouth)

plt.savefig("mini.png", dpi=150, bbox_inches='tight')
plt.show()
