clc; clear;
%model the gait of the snake
l = 1;
N = 11;

f = @(t,x) sin((x + t) * (2*pi / l)) * 0.25;

timespan = linspace(0,2*pi,1000);
xspan = linspace(0,l,N);
figure
grid on;
for i = timespan
    fxn_x = @(x) f(i,x);
    yspan = fxn_x(xspan);
    hold on
    plot(xspan,yspan);
    plot(xspan, yspan, 'r.', 'MarkerSize', 20) 
    xlim manual; ylim manual;
    xlim([-0.2 1.2]);
    ylim([-1.2 1.2]);
    pause(0.01);
    clf;
end


