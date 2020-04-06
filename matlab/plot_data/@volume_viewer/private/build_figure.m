function build_figure(obj)
% Initializes the volume viewer figure. Graphics object handles are stored
% in obj.handles. 

% Build a full screen figure window with a white color. 
obj.handles.figure = figure('Units','Normalized', ...
                            'Position',[0 0 1 1], ...
                            'Color', 'w');

% Set up the axes and image objects.
for ii = 1:3
    % Position vector: [x-coordinate,y-coordinate,x-size,y-size].
    position = [-0.15 + ii*0.25, 0.3, 0.25 0.25];
    
    % Create axes. 
    obj.handles.axes(ii) = axes('Units','Normalized', ...
                               'Position', position);
    
    % Permute image such that we always plot the first 2 dimensions. 
    % ii become the last dimension. 
    permuted_image = permute_image(obj.image,ii); 
    
    % Plot image. 
    obj.handles.images(ii) = imagesc(permuted_image(:,:,round(end/2)));
end

% Set up slice scroll bars. Whenever someone scrolls, the function
% slicescroll_callback (see below) will run. 
for ii = 1:3
    obj.handles.scrollbar(ii) = uicontrol('style', 'slider', ...
                                         'units','normalized', ...
                                         'position', [.05 + ii*0.25, .325 .05 .2]);%, ...
                                         %'callback', @(src,evt) slice_scroll_callback(src,evt,obj,1));
    addlistener(obj.handles.scrollbar(ii),'Value','PreSet', @(~,~) slice_scroll_callback(obj,ii));
end

% Make it all pretty.
set(obj.handles.axes                        , ...
    'DataAspectRatio'   , [1 1 1]           , ...
    'PlotBoxAspectRatio', [1 1 1]           , ...
    'Visible'           , 'off'             );    

% Draw everything before handing control back to the user.
drawnow
end
%% Support functions. 

function slice_scroll_callback(obj,idx)
% This function runs whenever the scrollbar is used. It will update the
% image to the slice indicated by the scroll bar. 

% Determine the new slice based on the value of the scrollbar. 
num_slices = size(obj.image,idx);
new_slice = 1 + round((num_slices-1) * obj.handles.scrollbar(idx).Value);

% Generate the permuted image (i.e. set idx to the last dimension).
permuted_image = permute_image(obj.image,idx); 

% Change the data of the image to the new slice. 
obj.handles.images(idx).CData = permuted_image(:,:,new_slice);  
end

function permuted_image = permute_image(image,dim)
% Generates a permuted image with dimension dim as the third dimension. 
dimensions = 1:3;
dimensions([3,dim]) = [dim,3]; 
permuted_image = permute(image, dimensions);
end