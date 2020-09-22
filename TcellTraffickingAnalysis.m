% F. Yang, E. Campillo-Funollet 2020

linux = 1;
o1 = 1;
o2 = 1;
format long
M = 10.0;
if(linux==0)
    cd(sprintf('flint_lab\\image analysis raw data',folder_list(folder_loop).name));
else
    cd(sprintf('flint_lab/image analysis raw data/'));
end

folder_list = dir;
is_folder = find(vertcat(folder_list.isdir));
[folder_size, folder_size_dummy] = size(is_folder);

myCellOne = zeros(50,50);
myCellTwo = zeros(50,50);
myCellThree = zeros(50,50);

for folder_loop = 3:folder_size
    folder_list(folder_loop).name
    cd(sprintf('%s',folder_list(folder_loop).name));
    
    img_sequence = 0; %frames/names may start with non-zero number
    figures_ext = '*.tif';
    figures_list = dir(figures_ext);
    [figures_list_size, figures_list_size_dummy] = size(figures_list);
    
    %% fwy: loop starts
    for img=1:figures_list_size
        %--------------------------------------------------------------------------
        file = figures_list(img).name;
        
        A = imread(file);
        A = A(1:998,:,:);
        R = A(:,:,1);
        G = A(:,:,2);
        
        %% Noise Reduction and Seg
        NRS = G;
        for i=1:200
            NRS = medfilt2(NRS);
        end
        level = graythresh(NRS);
        NRS = imbinarize(NRS, level);
        s = regionprops(NRS, 'All');
        format long
        Rhat3 = 0.0;
        denominator = 0.0;
        [A1, A2] = size(A);
        Rarea = A1*A2;
        if(numel(s)>0)
            for i = 1:numel(s)
                for j = 1:s(i).Area
                    denominator = denominator + double(R(s(i).PixelList(j,2), s(i).PixelList(j,1)));
                end
                
                if(Rarea*denominator>0)
                    for j = 1:s(i).Area
                        Rhat3 = Rhat3 + ...
                            ( double(R(s(i).PixelList(j,2), s(i).PixelList(j,1))) * s(i).Area * ...
                            exp( M * ( -( double(s(i).PixelList(j,2)-s(i).Centroid(1))^2 + ...
                            double(s(i).PixelList(j,1)-s(i).Centroid(2))^2) ) / ...
                            double( (s(i).MajorAxisLength/2.0)^2 + (s(i).MinorAxisLength/2.0)^2 ) ) ) / ...
                            ( denominator * Rarea );
                    end
                end
                denominator = 0.0;
            end
        else
            fprintf('Segmentation fault, 3 seg.\n');
        end
        
        if(o2==7) 
            o2 = 1;
            o1 = o1 + 1;
        end
        myCellThree(o1, o2) = Rhat3;
        o2 = o2 + 1;
        
        img_sequence = img_sequence + 1;
    end
    o1 = o1 + 2;
    cd('..');
end
