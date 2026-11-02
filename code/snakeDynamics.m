%%Parameters of the snake
L = 1; %total length of snake (m)
N = 11; % number of links in the snake
nJ = N-1; % number of joints in the snake
dl = L/(N); % discrete link length

clear VirtChassis; %clear any persistant variables?
clear; clc; close all;

%set up environment properties
timespan = linspace(0,1,200); %timespan to integrate over

figure
for i = timespan

    %calculate joint angles from the serpenoid equation
    joint_states = discreteJointAngles((1:nJ),i, nJ);
    
    %want absolute heading, adding relative headings for each joint
    phi = [0, cumsum(joint_states)];

    %points of snake joints
    points = [zeros(1,3); cumsum(dl*[cos(phi)', sin(phi)', zeros(nJ+1,1)], 1)];
    
    %find link centers
    link_centers = (points(1:end-1,:) + points(2:end,:))/2;

    %virtual chassis calcs, from REF 1
    [T] = VirtChassis(link_centers);

    %transform points into the virt chassis frame so we can view in that
    %frame
    pts_virt_frame = T \ [points'; ones(1, length(points))];
    pts_virt_frame = pts_virt_frame(1:3,:)';

    
    %plot
    hold on; grid on;
    plot(pts_virt_frame(:,1), pts_virt_frame(:,2), 'b-');
    plot(pts_virt_frame(:,1), pts_virt_frame(:,2), 'r.', 'MarkerSize', 20)
    plot(0,0, 'm.');
    xlabel("X position relative to Virtual Chassis (m)");
    ylabel("Y position relative to Virtual Chassis (m)");
    title("Snake Gait Animation wrt Virtual Chassis Frame");
    xlim manual; ylim manual; axis equal;
    xlim([-0.6 0.6]);
    ylim([-0.4 0.4]);
    pause(0.1);
    clf;
end