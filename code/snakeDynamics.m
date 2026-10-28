%%Parameters of the snake
L = 1; %total length of snake (m)
N = 11; % number of links in the snake
nJ = N-1; % number of joints in the snake
dl = L/(N); % discrete link length

%set up environment properties
timespan = linspace(0,1,200); %timespan to integrate over
