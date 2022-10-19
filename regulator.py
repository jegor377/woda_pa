import math
import matplotlib.pyplot as plt

def clamp(v, min_v, max_v):
    return min(max(v, min_v), max_v)

def actuator_voltage_to_input_quantity(actuator_voltage):
    return clamp(actuator_voltage, min_actuator_voltage, max_actuator_voltage) / actuator_voltage_range * max_input_quantity

def main():
    # parametry
    area = 1.5 # m^2
    beta = 0.035 # m^3 / s
    h = [0.0] # m
    desired_h = [4.0] # m
    deviation = [desired_h[-1] - h[-1]] # m
    delta_deviation = [0.0] # m
    # sterujace
    actuator_voltage = [0.0] # V
    # sterowane
    input_quantity = [max_input_quantity] # m^3 / s
    output_quantity = [0.0] # m^3 / s

    # zmienne
    t = [0.0] # s
    p_regulations = [0.0]
    i_regulations = [0.0]
    d_regulations = [0.0]

    N = int(simulation_time / sample_period) + 1
    mh = 0
    for i in range(1, N):
        t.append(i * sample_period)
        # wyznaczenie wartości uchybu regulacji
        deviation.append(desired_h[-1] - h[-1])
        delta_deviation.append(deviation[-1] - deviation[-2])
        # wyznaczenie wartości sterującej regulatora
        # actuator_voltage.append(regulator_gain * deviation[-1]) # przyklad regulatora typu P
        # actuator_voltage.append(regulator_gain * (deviation[-1] + sample_period / doubling_time * sum(deviation))) # przyklad regulatora typu PI
        p_regulations.append(regulator_gain * deviation[-1])
        i_regulations.append(regulator_gain * sample_period / doubling_time * sum(deviation))
        d_regulations.append(regulator_gain * lead_time / sample_period * delta_deviation[-1])
        actuator_voltage.append(p_regulations[-1] + i_regulations[-1] + d_regulations[-1]) # przyklad regulatora typu PID
        # wyznaczenie doplywu
        input_quantity.append(actuator_voltage_to_input_quantity(actuator_voltage[-1]))
        # wyznaczenie odplywu
        output_quantity.append(beta * math.sqrt(h[-1]))
        # wyznaczenie nowego poziomu wody
        new_height = sample_period / area * (input_quantity[-1] - output_quantity[-1]) + h[-1]
        if abs(new_height) == math.inf:
            raise ValueError(new_height)
        if new_height < h_min:
            print(f"Woda spadła poniżej wartości minimalnej: {new_height}m {t[-1]}s")
        elif new_height > h_max:
            print(f'Woda wzrosła powyżej wartości maksymalnej: {new_height}m {t[-1]}s')
        h.append(min(max(new_height, h_min), h_max))
        mh = max(mh, h[-1])
        if i * sample_period > 2000 and i * sample_period < 3000:
            desired_h.append(1.5)
        elif i * sample_period > 3000:
            desired_h.append(5.0)
    plt.plot(t, h)
    plt.savefig("height.png", dpi=96 * 10)
    plt.clf()
    plt.legend(['p', 'i', 'd'])
    plt.plot(t, p_regulations, label='p')
    plt.plot(t, i_regulations, label='i')
    plt.plot(t, d_regulations, label='d')
    # plt.plot(t, actuator_voltage, label='av')
    plt.legend()
    plt.savefig("regulator.png", dpi=96 * 10)
    print(mh, (mh - desired_h[-1]) / desired_h[-1])

if __name__ == '__main__':
    # stałe
    h_max = 10.0 # m
    h_min = 0.0 # m
    max_actuator_voltage = 5.0 # V
    min_actuator_voltage = 0.0 # V
    actuator_voltage_range = max_actuator_voltage - min_actuator_voltage
    max_input_quantity = 0.5 # m^3 / s
    sample_period = 0.1 # s
    simulation_time = 3600.0 # s
    regulator_gain = 10
    doubling_time = 7
    lead_time = 10
    main()
