import numpy as np
import matplotlib.pyplot as plt

def main():
    J1 = 2.2
    J2 = 1
    B1 = 3
    Kt = 2
    M = 16
    b = 2
    k = 20
    R = 0.5
    r = 0.1
    m = r

    # define the system ODEs
    def equations(x, t):
        line_1 = np.array([-B1/J1, 0, -Kt, 0])
        convt = (1 + M*m**2/J2)
        line_2 = np.array([0, -m**2*b/J2/convt, Kt/convt, -m*k/convt])
        line_3 = np.array([1/J1, -1/J2, 0, 0])
        line_4 = np.array([0, m/J2, 0, 0])

        A = np.array([line_1, line_2, line_3, line_4])
        B = np.array([1, 0, 0, 0])
        t_in = 5 if t < 25 else 0
        return np.dot(A, x) + B * t_in
    x0 = np.array([0, 0, 0, 0])

    t = np.array([x*0.01 for x in range(5000)])

    sol = rk4fixed(equations, x0, t)
    fig, (ax1, ax2) = plt.subplots(2)
    p3 = sol[:,0]
    p7 = sol[:,1]
    p10 = M*m*p7/J2
    q5 = sol[:,2]
    q11 = sol[:,3]
    twist = q5-q11

    dots = np.array([equations(sol[i],t[i]) for i in range(len(sol))])
    p7_dot = dots[:,1]
    p10_dot = M*m*p7_dot/J2

    ax1.plot(t, twist, label = "Twist angle (rad)")
    ax1.plot(t, p10, label = "Mass displacement (m)")
    ax1.legend()
    ax1.set_title("__ vs Time")
    ax1.set_xlabel("Time (s)")
    ax1.grid()

    ax2.plot(t,p10_dot, label = "Mass velocity (m/s)")
    ax2.plot(t,dots[:,2] - dots[:,3], label = "Twist rate (rad/s)")
    ax2.grid()
    ax2.set_title("__ vs Time")
    ax2.set_xlabel("Time (s)")
    ax2.legend()
    plt.show()
    

def rk4fixed(f, x0, t):
    import numpy
    n = len(t)
    x = numpy.zeros((n, len(x0)))
    x[0] = x0
    for i in range(n - 1):
        h = t[i+1] - t[i]
        k1 = f(x[i], t[i])
        k2 = f(x[i] + k1 * h / 2., t[i] + h / 2.)
        k3 = f(x[i] + k2 * h / 2., t[i] + h / 2.)
        k4 = f(x[i] + k3 * h, t[i] + h)
        x[i+1] = x[i] + (h / 6.) * (k1 + 2*k2 + 2*k3 + k4)
    return x

if __name__ == "__main__":
    main()