function mapll,xy,latitude,longitude
    
    RE = 6378.273
    E2 = 0.006693883
    PI = 3.141592654
    E  = sqrt(E2)
    
    if abs(latitude) lt PI/2 then begin
       SL = 70 * PI / 180
       T  = tan(PI/4 - latitude/2) / ((1- E*sin(latitude)) / (1+ E*sin(latitude)))^(E/2)      
       TC = tan(PI/4 - SL/2)  / ((1 - E*sin(SL)) / (1 + E*sin(SL)))^(E/2)
       MC = cos(SL) / sqrt(1.0 - E2*(sin(SL)^2))
       RHO = RE * MC * T / TC
       
       xy[1] = -RHO  * cos(longitude)
       xy[0] =  RHO  * sin(longitude)
       
    endif
    
    return,xy
    
end

PRO projection_tb_FY3B
device, decomposed = 1
    read_png,'E:\973-snow\data\input\colorbar\N-AMSR_E_L3_SeaIce12km_V11_20090605.png',pal,r,g,b
    tvlct,r,g,b
    
    landmask_n  = intarr(896,608)
           
    sd_id_n = HDF_SD_START('E:\973-snow\data\input\amsr_landmask_12n.hdf')
    
    index = hdf_sd_nametoindex(sd_id_n,'landmask')
    sds_id_n=HDF_SD_SELECT(sd_id_n,index)
    HDF_SD_GETDATA,sds_id_n,data
    landmask_n = data
    HDF_SD_ENDACCESS,sds_id_n   
    
    coast_n  = bytarr(608,896)
    flag_mysi = intarr(608,896)
    
    openr,fin_id, 'E:\973-snow\data\input\coast_n.txt',/get_lun
    readu,fin_id,coast_n
    close,fin_id   
        
    index_land_n = where((landmask_n eq 1) or (coast_n eq 1))    
    
    file  = HDF_OPEN('E:\973-snow\data\input\multiyear sea ice flag_2009.hdf')
    sd_id = HDF_SD_START('E:\973-snow\data\input\multiyear sea ice flag_2009.hdf')
    
    index = hdf_sd_nametoindex(sd_id,'flag_seaice_nh')
    sds_id_n=HDF_SD_SELECT(sd_id,index)
    HDF_SD_GETDATA,sds_id_n,data
    flag_mysi = data
    HDF_SD_ENDACCESS,sds_id_n 
    hdf_close,file
    
    
    dir_readed_tb = 'E:\973-snow\data\MWRI\readed\' 
    dir_project_tb = 'E:\973-snow\data\MWRI\projected\' 
    out_picture = 'E:\973-snow\data\MWRI\picture\'

    filename = FILE_SEARCH( dir_readed_tb + '*201109*.txt', COUNT=cnt )
        
    for id_f = 0,cnt-1 do begin 
       
       Time = strmid(filename[id_f],11,8,/reverse)
       year = strmid(time,0,4)
       year = fix(year)
       mon = strmid(time,4,2)
       mon = fix(mon)
         
       ;定义经纬度、密集度、各通道亮温数据的数组
       lat  = fltarr(608,896)
       lon  = fltarr(608,896)
       icecon_total = fltarr(608,896)
       SIC = intarr(608,896)
       
       V107 =   fltarr(608,896)
       H107 =   fltarr(608,896)
       V187 =   fltarr(608,896)
       H187 =   fltarr(608,896)
       V238 =   fltarr(608,896)
       H238 =   fltarr(608,896)
       V365 =   fltarr(608,896)
       H365 =   fltarr(608,896)
       H890 =   fltarr(608,896)
       V890 =   fltarr(608,896)     
       num =    intarr(608,896)
       num_sic = intarr(608,896)
       snowdepth = intarr(608,896)       

       
       a = ''
       a_d = ''
       openr, finid,  filename[id_f], /get_lun
       readf, finid,  format = '(a60)',a       
        
                 
          RE = 6378.273
          E2 = 0.006693883
          PI = 3.141592654
          E  = sqrt(E2)
          
       while not eof(finid) do begin
          
          ;读取存储的亮温数据
          readf,finid,format = '(2F10.3,a10,10f8.2)',lat1,lon1,a_d,V107_Res3,H107_Res3,V187_Res3,$
                               H187_Res3,V238_Res3,H238_Res3,V365_Res3,H365_Res3,V890_Res3,H890_Res3      
               
          ;将密集度数据投影到极射投影网格内
          x = 0
          y = 0
          
          if lon1 lt 0.0 then lon1 = lon1 + 360

          
          lat_a = lat1
          lon_a = lon1             
          
          lon1 = (lon1 + 45) * PI / 180 
          m = 608
          n = 896  
          
          lat1 = abs(lat1) * PI / 180
          
          xy = intarr(2)
          ;计算对应xy值
          xy =  mapll(xy,lat1,lon1)
          
          x = xy[0]
          y = xy[1]             
          
          i = fix(( x + 3850 - 12.5/2.0) / 12.5) + 1
          k = fix(( y + 5350 - 12.5/2.0) / 12.5) + 1  
          j = 896 - k +1                
          
          ;对落入网格内的点进行求和处理
          if (i le m) and (j le n) and (i ge 1) and (j ge 1) then begin
              num[i-1,j-1] = num[i-1,j-1] + 1          
              lat[i-1,j-1] = lat[i-1,j-1] + lat_a
              lon[i-1,j-1] = lon[i-1,j-1] + lon_a
              V107[i-1,j-1] = V107[i-1,j-1]  + V107_Res3
              H107[i-1,j-1] = H107[i-1,j-1]  + H107_Res3          
              V187[i-1,j-1] = V187[i-1,j-1]  + V187_Res3
              H187[i-1,j-1] = H187[i-1,j-1]  + H187_Res3             
              V238[i-1,j-1] = V238[i-1,j-1]  + V238_Res3 
              H238[i-1,j-1] = H238[i-1,j-1]  + H238_Res3            
              V365[i-1,j-1] = V365[i-1,j-1]  + V365_Res3 
              H365[i-1,j-1] = H365[i-1,j-1]  + H365_Res3         
              V890[i-1,j-1] = V890[i-1,j-1]  + V890_Res3             
              H890[i-1,j-1] = H890[i-1,j-1]  + H890_Res3 
         endif
          
       endwhile  
         
       free_lun, finid       
       
       ;对有数据点的网格内数据进行平均处理
       index = where(num gt 0,COMPLEMENT=index_non)
       lat[index]  =  lat[index] / num[index]
       lon[index]  =  lon[index] / num[index]                
       V107[index] = V107[index] / num[index] 
       H107[index] = H107[index] / num[index]                
       V187[index] = V187[index] / num[index] 
       H187[index] = H187[index] / num[index]
       V238[index] = V238[index] / num[index]
       H238[index] = H238[index] / num[index]
       V365[index] = V365[index] / num[index]
       H365[index] = H365[index] / num[index]
       V890[index] = V890[index] / num[index]
       H890[index] = H890[index] / num[index]
       
       ;对于无数据点的网格，设定各通道亮温值为-1
       index_mis =  where(num eq 0 ,cont_mis)
       if cont_mis ne 0 then begin 
          lat[index_mis]  = -1
          lon[index_mis]  = -1                
          V107[index_mis] = -1 
          H107[index_mis] = -1               
          V187[index_mis] = -1 
          H187[index_mis] = -1
          V238[index_mis] = -1
          H238[index_mis] = -1
          V365[index_mis] = -1
          H365[index_mis] = -1
          V890[index_mis] = -1
          H890[index_mis] = -1           
       endif
      
      ;输出各通道日均亮温数据、海冰密集度及积雪深度数据
       file = dir_project_tb + 'FY3B_MWRI_' + time + '.h5'
       fid = H5F_CREATE(file)
       
       datatype_id = H5T_IDL_CREATE(lat)
       dataspace_id = H5S_CREATE_SIMPLE(size(lat,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'Latitude',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,lat        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id
       H5D_CLOSE,dataset_id
       
       datatype_id = H5T_IDL_CREATE(lon)
       dataspace_id = H5S_CREATE_SIMPLE(size(lon,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'Longitude',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,lon        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id
       H5D_CLOSE,dataset_id
       
       datatype_id = H5T_IDL_CREATE(V107)
       dataspace_id = H5S_CREATE_SIMPLE(size(V107,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'V107_TB',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,V107        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id
       H5D_CLOSE,dataset_id
       
       datatype_id = H5T_IDL_CREATE(H107)
       dataspace_id = H5S_CREATE_SIMPLE(size(H107,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'H107_TB',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,H107        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id
       H5D_CLOSE,dataset_id
       
       datatype_id = H5T_IDL_CREATE(V187)
       dataspace_id = H5S_CREATE_SIMPLE(size(V187,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'V187_TB',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,V187        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id
       H5D_CLOSE,dataset_id
       
       datatype_id = H5T_IDL_CREATE(H187)
       dataspace_id = H5S_CREATE_SIMPLE(size(H187,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'H187_TB',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,H187        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id
       H5D_CLOSE,dataset_id
       
       datatype_id = H5T_IDL_CREATE(V238)
       dataspace_id = H5S_CREATE_SIMPLE(size(V238,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'V238_TB',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,V238        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id
       H5D_CLOSE,dataset_id
              
       datatype_id = H5T_IDL_CREATE(H238)
       dataspace_id = H5S_CREATE_SIMPLE(size(H238,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'H238_TB',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,H238        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id
       H5D_CLOSE,dataset_id
       
       datatype_id = H5T_IDL_CREATE(V365)
       dataspace_id = H5S_CREATE_SIMPLE(size(V365,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'V365_TB',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,V365        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id
       H5D_CLOSE,dataset_id
       
       datatype_id = H5T_IDL_CREATE(H365)
       dataspace_id = H5S_CREATE_SIMPLE(size(H365,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'H365_TB',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,H365        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id
       H5D_CLOSE,dataset_id
       
       datatype_id = H5T_IDL_CREATE(V890)
       dataspace_id = H5S_CREATE_SIMPLE(size(V890,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'V890_TB',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,V890        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id
       H5D_CLOSE,dataset_id
       
       datatype_id = H5T_IDL_CREATE(H890)
       dataspace_id = H5S_CREATE_SIMPLE(size(H890,/DIMENSIONS))
       dataset_id = H5D_CREATE(fid,'H890_TB',datatype_id,dataspace_id)
       H5D_WRITE,dataset_id,H890        
       H5S_CLOSE,dataspace_id
       H5T_CLOSE,datatype_id       
       H5D_CLOSE,dataset_id
       
       H5F_CLOSE,fid
   
       tb_nh = fltarr(608,896,10)
       
       name = strarr(10)
       
       tb_nh[*,*,0] = V107
       tb_nh[*,*,1] = H107
       tb_nh[*,*,2] = V187
       tb_nh[*,*,3] = H187
       tb_nh[*,*,4] = V238
       tb_nh[*,*,5] = H238
       tb_nh[*,*,6] = V365
       tb_nh[*,*,7] = H365
       tb_nh[*,*,8] = V890
       tb_nh[*,*,9] = H890
                   
       name = ['V107','H107','V187','H187','V238','H238','V365','H365','v890','H890']
                     
       bardata=indgen(190)+1
       colorbar=replicate(1b,20)#bardata
             
       ;display the tb data
       
       
       tb_temp = fltarr(608,896)
       bar=congrid(colorbar,30,896)
       cb =intarr(608,896)
       
       for id_tb = 0 ,9 do begin
          
          tb_temp = tb_nh[*,*,id_tb]
       
          tb_temp = bytscl(tb_temp,0, max =300, top=190)
          ;tb_temp[index_land]  = 254  
          
          window,1,XSIZE=785, YSIZE=1036,title = 'Brightness Temperature of North Hemisphere in' + name[id_tb] + 'Channel',/pixmap
          ERASE
          tv,tb_temp,50,50,/device,/Order
          contour,cb,yrange=[ 0,168],xrange=[ 279,350],position = [50, 50, 658, 946],yticklen=0.001,xticklen=0.001, /NOERASE, /DEVICE, font=0,$
                  xticks =1,xminor=0,yticks=1,yminor=0,xstyle=1,ystyle=1,$
                  xtickname=['lon:279.26','lon:350.03'], ytickname=[' ',' ']
                  
          xyouts,20,955,'lon:168.35 ' ,color=250,/device,charsize=2,font=0
          xyouts,620,955,'lon:102.34 ' ,color=250,/device,charsize=2,font=0
          xyouts,250,1000,'Brightness Temperature of '+ name[id_tb] + ' Channel',color=250,/device,charsize=4,font=0
          xyouts,325,970, 'Date: ' + time ,color=250,/device,charsize=3,font=0
          
          tv,bar,708,50
          xyouts,720,948,'k',color=250,/device,charsize=3,font=0
          CONTOUR, bar, yrange=[ 0,300], ystyle=1,  xstyle=1,level=[300], $
                   position = [708,50,738,946], /NOERASE, /DEVICE,  font=0, $
                   yticklen=0.1,yminor=10,xticks=1,yticks=6,$
                   xtickname = [' ',' '], ytickname = ['0 ',' 50','100',' 150',' 200',' 250',' 300']
            
          write_png, out_picture + name[id_tb] + time + '_' + strcompress(a_d,/remove_all) + '.png',TVRD(),r,g,b
          WDELETE,1 
       
       endfor 
   
    endfor
   
    print,'ok'
   
end

