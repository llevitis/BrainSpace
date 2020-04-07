function slice = get_slice(obj,dim)
% Grabs the current slice given a particular orientation (dim).
% Kept in a separate function to make sure any rotations/flips are
% identical across all calls.

img = obj.image;
if dim == 1
    slice = squeeze(img(obj.slices(dim),:,:));
elseif dim == 2
    slice = squeeze(img(:,obj.slices(dim),:));
elseif dim == 3
    slice = squeeze(img(:,:,obj.slices(dim)));
else 
    error('dim must be 1, 2, or 3');
end
end