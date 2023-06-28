# soil_process

​	该项目为时空大数据分析与处理课程实习 第一节 VIC水文模型原理与应用，我研发的处理土壤数据空缺的小程序。

​	在计算土壤参数时，需要对H_T_USDA，H_S_USDA两个关键参数进行空值填充。但是使用Excel中难以实现顾及地块空间近邻关系的空值填充，而ArcGIS中的工具提供了对栅格数据属性值的平滑方法，但是我们需要填补的是地块的类别标签而不是计算属性值，并且这一工具使用的限制条件较多。

​	问题分析：首先是土壤POI“点转栅格”造成的间隙，会导致存在一些全为-1的行和列，这部分数据对后续处理造成干扰。因此需要找出这些行和列，并将其删除。其次，当土壤数据存在大片的、连续的空值需要填充时，小尺寸的窗口可能无法实现非零填充（例如，当窗口中大部分元素都为0或-1时）。为此，在无法填充时需要扩大窗口尺寸，实现可变尺度的空间滤波。此外，当缺失值过多时，一轮迭代可能无法完成全部土壤单元的填充，算法需要支持多次迭代。

​    故本次实习中，我针对上述问题使用Python编程的方式，实现一种可变尺度的空间滤波空值填充迭代算法。

​    算法流程如下：

1. 初始化参数：在开始时，选择填充的参数，可以选择 'H_T_USDA' 或 'H_S_USDA'。 

2. 读取图像数据：使用tifffile库的imread方法读取图像文件，并将其转化为numpy数组。 

3. 读取CSV文件：读取一个包含土壤信息的CSV文件，其中将'#N/A'视为缺失值，并用0来填充这些缺失值。 

4. 替换图像中的特定值：使用CSV文件中的数据，找到图像中与CSV文件中的'GRID'列相匹配的值，并将这些值替换为'H_T_USDA'或者'H_S_USDA'的值。 

5. 删除间隙：删除图像中全为-1的行和列。这一步操作是为了去除点转栅格造成的间隙。 

6. 保存原始图像：将处理过的图像数据保存为CSV文件。 

7. 创建过滤器函数：创建一个过滤器函数，用于后续的图像填充操作。如果中心像素是0，则返回窗口像素中非-1的众数。否则，返回中心像素的值。 

8. 创建新的图像以保存结果：复制原始图像数据，以创建一个新的图像，用于保存处理结果。 

9. 图像填充操作：进行两层迭代，内层迭代进行图像填充，外层迭代用于调整窗口大小，若无法完成填充，则逐步扩大窗口大小，直到图像中没有0值。 

10. 保存处理后的图像：将处理后的图像保存为CSV文件。 

11. 找出所有非-1的像素并保存：找出处理后的图像中所有非-1的像素，并将这些像素转换为一维数组，然后保存为CSV文件。 



------



This project is a small program I developed for the first session of the course on Spatio-temporal Big Data Analysis and Processing, titled "Principles and Applications of the VIC Hydrological Model", to deal with missing soil data.

When calculating soil parameters, it's necessary to fill in missing values for two key parameters: H_T_USDA and H_S_USDA. However, it is challenging to consider spatial neighborhood relationships when filling in missing values in Excel. Although the tools in ArcGIS provide a smoothing method for raster data attribute values, what we need to fill in is the category label of the plot rather than the calculated attribute value, and the conditions for using this tool are quite restrictive.

Problem Analysis: Firstly, the gaps caused by the "Point to Raster" transformation of soil POI will lead to some rows and columns that are entirely -1, and these data can interfere with subsequent processing. Hence, it's necessary to find and delete these rows and columns. Secondly, when a large, continuous block of soil data needs to be filled, a small window may not achieve non-zero filling (e.g., when most of the elements in the window are 0 or -1). Therefore, the window size needs to be expanded when filling is not possible to implement variable scale spatial filtering. In addition, when there are too many missing values, one round of iteration may not complete the filling of all soil units, so the algorithm needs to support multiple iterations.

Therefore, during this internship, I used Python to implement an iterative algorithm for filling in missing values using variable scale spatial filtering to address the above issues.

The algorithm process is as follows:

1. Initialize parameters: At the start, select the parameter to be filled, which can be 'H_T_USDA' or 'H_S_USDA'.
2. Read image data: Use the imread method from the tifffile library to read the image file and convert it into a numpy array.
3. Read CSV file: Read a CSV file containing soil information. Consider '#N/A' as missing values and fill these missing values with 0.
4. Replace specific values in the image: Use the data from the CSV file to find values in the image that match the 'GRID' column in the CSV file, and replace these values with the 'H_T_USDA' or 'H_S_USDA' values.
5. Delete gaps: Delete rows and columns in the image that are entirely -1. This step is to remove the gaps caused by the point-to-raster conversion.
6. Save the original image: Save the processed image data as a CSV file.
7. Create a filter function: Create a filter function for the subsequent image filling operation. If the central pixel is 0, return the mode of the window pixels that are not -1. Otherwise, return the value of the central pixel.
8. Create a new image to save results: Copy the original image data to create a new image for saving the processing results.
9. Image filling operation: Conduct two layers of iterations. The inner iteration performs image filling, and the outer iteration adjusts the window size. If the filling cannot be completed, gradually increase the window size until there are no 0 values in the image.
10. Save the processed image: Save the processed image as a CSV file.
11. Find all non-1 pixels and save: Find all non-1 pixels in the processed image, convert these pixels into a one-dimensional array, and save them as a CSV file.
