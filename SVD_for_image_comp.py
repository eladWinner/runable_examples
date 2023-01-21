from PIL import Image
import numpy as np
import random

image_path =r"complex-futuristic-information-data.jpg" # in project folder
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #load picture
    image = Image.open(image_path)
    if image.mode !='RGB':
        exit("wrong image type!")
    width = image.width
    height = image.height
    picture_data = np.array(image)
    RGB_svds=[]
    RGB_singulars_squared=[]
    #find svd for each color
    for i in range(3):
        RGB_svds.append(np.linalg.svd(picture_data[:,:,i]))
        singulars_squared =[j ** 2 for j in RGB_svds[i][1]]
        RGB_singulars_squared.append([sum(singulars_squared),singulars_squared])
    errors = {}
    size_limit =min(width,height)
    #test for a few K values
    k_list = []
    two_pow=1
    while((height/two_pow).is_integer() and (width/two_pow).is_integer()):
        k_list.append(int(size_limit/two_pow))
        two_pow*=2
    hand_picked=[475,485,500]
    for i in hand_picked:
        k_list.append(i)
    for k in k_list:
        if k > size_limit:
            continue
        #create 3D matrix same size as picture
        result_image = np.zeros((height,width,3))
        #create k sized one color picture
        for i in range(3):
            one_color_image = np.zeros((height,width))
            for j in range(k): # only take first k self values
                one_color_image[j][j]=RGB_svds[i][1][j]
            one_color_image=np.matmul(RGB_svds[i][0],np.matmul(one_color_image,RGB_svds[i][2]))
            #add color layer to empty image
            result_image[:,:,i] = one_color_image
        # save result
        result_image_file = Image.fromarray(result_image.astype('uint8'))
        # find error ..... sum of first K squared singular /   sum of all SS
        errors[k] = sum(RGB_singulars_squared[i][1][k+1:])/RGB_singulars_squared[i][0]
        result_image_file.save("K="+str(k)+",errors="+str(round(errors[k],6))+"_results_image.png")

    for k in errors:
        print(k, errors[k])

