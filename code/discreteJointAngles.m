function [theta] = discreteJointAngles(i, t, joints)
    %based on REF 1, on serepenoid angle
    Beta = 0;
    Amp = 0.5;
    omega = 2*pi / joints;
    v = 2*pi;
    si = omega * i + v * t;

    theta = Beta + Amp*sin(si);
end