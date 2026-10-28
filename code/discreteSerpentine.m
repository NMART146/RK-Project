clear; clc;

L = 1;
N = 11;
nJ = N-1;
dl = L/(N);
timespan = linspace(0,1,200);

figure
grid on;


for i = timespan
    thetas = discreteJointAngles((1:nJ),i, nJ);
    phi = [0, cumsum(thetas)]; %absolute heading, adding relative headings
    points = [zeros(1,3); cumsum(dl*[cos(phi)', sin(phi)', zeros(nJ+1,1)], 1)]; %points of snake joints

    %virtual chassis calcs
    [T] = VirtChassis(points);

    %transform points into the virt chassis frame
    pts_virt_frame = T \ [points'; ones(1, length(points))];
    pts_virt_frame = pts_virt_frame(1:3,:)';

    virt_chassis_location = T(1:2,4);
    

    %plot
    hold on
    plot(pts_virt_frame(:,1), pts_virt_frame(:,2), 'b-');
    plot(pts_virt_frame(:,1), pts_virt_frame(:,2), 'r.', 'MarkerSize', 20)
    plot(virt_chassis_location(1), virt_chassis_location(2), 'm.');
    xlim manual; ylim manual; axis equal;
    xlim([-1 1]);
    ylim([-1 1]);
    pause(0.1);
    clf;
end

