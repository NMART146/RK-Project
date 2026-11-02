function [theta] = snakePose(absolute_joint_states)
    %Construct Helper Matricies
    n = length(absolute_joint_states);
    A = zeros(n-1,n);
    D = zeros(n-1,n);

    for i = 1:n-1
        A(i,i) = 1; %make diag +1
        D(i,i) = 1; %make diag +1

        A(i,i+1) = 1; %make +1 off-diag +1
        D(i,i+1) = -1; %make +1 off-diag -1
    end
    
    e = ones(n,1);
    E = [e, zeros(n,1);
         zeros(n,1), e];

    stheta = sin(absolute_joint_states);
    ctheta = cos(absolute_joint_states);
    Stheta = diag(stheta);
    Ctheta = diag(ctheta);

    V = A' * ((D*D')\A);
    N = A' * ((D*D')\D);

end