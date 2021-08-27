imageRGB = imread("map.bmp");
imageGray = rgb2gray(imageRGB);
binImage = imageGray <0.5;
grid = binaryOccupancyMap(binImage, 50);
show(grid)
saveas(gcf, "grid.bmp")

robotRadius = 0.177;
fatGrid = copy(grid);
inflate(fatGrid, robotRadius);
show(fatGrid)
saveas(gcf, 'fatGrid.bmp')