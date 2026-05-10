from physics import *
from animation import *

traj, energies = string(100, 10000, 0.5, 18000, 120, 0.01, damping=0.1, count_energy=True)

plt.plot(energies)
plt.xlabel("шаг")
plt.ylabel("полная энергия")
plt.title("Сохранение энергии")
plt.savefig("energy.png")

animate_particles(traj, 120, speed=6) # внутри animate_particles вызывается plt.show() и показываются все созданные графики