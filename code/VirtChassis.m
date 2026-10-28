function [T] = VirtChassis(joint_locations)

    persistent V_last; %found out this keeps a persistant variable between fxn calls
    %constructs the "virtual chassis" as defined by REF1
    geo_center = sum(joint_locations) ./ (length(joint_locations));
    
    p_matrix = joint_locations - geo_center;

    [~,~,V] = svd(p_matrix, 'econ');

    %solve for positive and right handed V
    if ~isempty(V_last)
        if dot(V(:,1), V_last(:,1)) < 0
            V(:,1) = -V(:,1);
        end
        
        if dot(V(:,2), V_last(:,2)) < 0
            V(:,2) = -V(:,2);
        end

    end

    V(:,3) = cross(V(:,1),V(:,2));
    V_last = V;

    T = [V, geo_center';
         0,0,0,1];
end