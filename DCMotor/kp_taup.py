def kp_taup_calculator():
    Kt = 0.0109
    r=1.5506
    Je=0.0094
    n_s =1 #numeral que multiplica o s no denominador

    print("\nEquação antes da manipulação")
    omega_s = Kt/(r*Je)
    print("numerador:", omega_s)

    U_s = (Kt*Kt)/(r*Je)
    print("demoninador:", n_s, "s + ",U_s)
    print("---------------------------")

    omega_s=omega_s/U_s #manipulação algébrica para deixar a constante de tempo multiplicando o s no denominador

    n_s= n_s/U_s
    U_s=1

    print("\nEquação pós manipulação")
    print("numerador:", omega_s)
    print("demoninador:", n_s, "s + ",U_s)
    print("---------------------------")

    #Com essa manipulação tem-se que kp = omega_s
    #e a constante de tempo taup é n_s

    return omega_s, n_s




