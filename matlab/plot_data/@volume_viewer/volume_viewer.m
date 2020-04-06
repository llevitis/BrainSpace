classdef volume_viewer < handle
    
    %% Properties of the class (i.e. stored variables).
    % Properties that the user may not modify.
    properties(SetAccess = private)
        image % Should only be defined at initialization.
    end
    
    % Properties that the user may modify. 
    properties
        handles % Lets advanced users modify things like figure color. 
    end
    
    %% Methods of the class (i.e. functions). 
    methods
        function obj = volume_viewer(varargin)
            % Constructor function; this runs when the object is first
            % created. 
            
            % Parse the input.
            is_3d_numeric = @(x)numel(size(x)) == 3 && isnumeric(x); 
            p = inputParser();
            addRequired(p,'image',is_3d_numeric)
            
            % Example for adding required arguments:
            %addRequired(p,'PropertyName',function_checking_correct_input)
            % Example for adding optional arguments:
            %addParameter(p,'PropertyName','default_value',function_checking_correct_input)
                   
            parse(p, varargin{:}); 
                     
            % Set the object properties.
            obj.image = p.Results.image;
            obj.handles = struct('figure',gobjects(0), ...
                                 'axes', gobjects(0)); 
                                 % Add other handles as required. 
    
            % Initialize figure. 
            obj.build_figure();
        end
    end
end