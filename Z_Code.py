import numpy as np
import geopandas as gpd
from shapely.geometry import LineString, MultiPoint, Point
import matplotlib.pyplot as plt
import momepy
import networkx as nx
import pandas as pd
from string import ascii_letters as ABC 
import matplotlib.cm as cm


###START Parameters START###
# Poisson line process parameters
lambda0 = 1;  # intensity (ie mean density) of the Poisson line process
mu = 2;
tau=1;
ev_mu=0;
ev_sigma=0.06;
# Simulation disk dimensions
xx0 = 0;
yy0 = 0;  # center of disk
radius=1;
rth=0.4
massLine = 2 * np.pi * radius * lambda0;  # total measure/mass of the line process
###END Parameters END###

###START Simulate a Poisson line process on a disk START###
# Simulate Poisson point process
numbLines = np.random.poisson(massLine);  # Poisson number of points

# plot circle
t = np.linspace(0, 2 * np.pi, 200);
xp = radius * np.cos(t);
yp = radius * np.sin(t);

cars_x =[]
cars_y=[]
chrgr_x=[]
chrgr_y=[]


def isBetween(a, b, c):
    ax = a[0]
    bx= b[0]
    cx=c[0]
    ay=a[1]
    by=b[1]
    cy=c[1]
    crossproduct = (cy - ay) * (bx - ax) - (cx - ax) * (by - ay)

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) > 0.01:
        return False

    dotproduct = (cx - ax) * (bx - ax) + (cy - ay)*(by - ay)
    if dotproduct < 0:
        return False

    squaredlengthba = (bx - ax)*(bx - ax) + (by - ay)*(by - ay)
    if dotproduct > squaredlengthba:
        return False

    return True


def generate_random_line_within_circle(radius):
    # Generate random angle
    theta = 2 * np.pi * np.random.rand(1)
    # Generate random radius
    p = radius * np.random.rand(1);
    q = np.sqrt(radius ** 2 - p ** 2);
    sin_theta = np.sin(theta);
    cos_theta = np.cos(theta);
    ###START Simulate a Poisson point processes on each line START###
    lengthLine = 2 * q;  # length of each segment
    massPoint = mu * lengthLine;  # mass on each line
    numbLinePoints = np.random.poisson(massPoint);  # Poisson number of points on each line
    numbLinePointsTotal = sum(numbLinePoints);
    uu = 2 * np.random.rand(numbLinePointsTotal) - 1;  # uniform variables on (-1,1)

    # replicate values to simulate points all in one step
    xx0_all = np.repeat(xx0, numbLinePointsTotal);
    yy0_all = np.repeat(yy0, numbLinePointsTotal);
    p_all = np.repeat(p, numbLinePoints);
    q_all = np.repeat(q, numbLinePoints);
    sin_theta_all = np.repeat(sin_theta, numbLinePoints);
    cos_theta_all = np.repeat(cos_theta, numbLinePoints);

    # position points on Poisson lines/segments
    xxPP_all = xx0_all + p_all * cos_theta_all + q_all * uu * sin_theta_all;
    yyPP_all = yy0_all + p_all * sin_theta_all - q_all * uu * cos_theta_all;
    
    cars_x.append(xxPP_all)
    cars_y.append(yyPP_all)
    
    mP = tau * lengthLine; 
    nP = np.random.poisson(mP);  # Poisson number of points on each line
    nPoints = sum(nP);
    uev = 2 * np.random.rand(nPoints) - 1;  # uniform variables on (-1,1)

    # replicate values to simulate points all in one step
    xev0 = np.repeat(xx0, nPoints);
    yev0 = np.repeat(yy0, nPoints);
    rtemp=ev_sigma*np.random.rand()
   # ptemp= p+rtemp
    #if(ptemp>radius):
        #ptemp=ptemp-2*rtemp
    p_ev = np.repeat(p, nPoints);
    q_ev = np.repeat(q, nPoints);
    sin_theta_ev = np.repeat(sin_theta, nPoints);
    cos_theta_ev = np.repeat(cos_theta, nPoints);

    # position points on Poisson lines/segments
    xev = xev0 + p_ev * cos_theta_ev + q_ev * uev * sin_theta_ev;
    yev = yev0 + p_ev * sin_theta_ev - q_ev * uev * cos_theta_ev;
    #xev = xev+ np.random.normal(ev_mu, ev_sigma, 1)
    #yev = yev+ np.random.normal(ev_mu, ev_sigma, 1)
    
    chrgr_x.append(xev)
    chrgr_y.append(yev)
    # Calculate random points within the circle
    x1, y1 = xx0 + p * cos_theta + q * sin_theta, yy0 + p * sin_theta - q * cos_theta
    x2, y2 = xx0 + p * cos_theta - q * sin_theta, yy0 + p * sin_theta + q * cos_theta
   
    return LineString([(x1, y1), (x2, y2)])

# Generate Poisson process of random lines within a unit circle
lines = [generate_random_line_within_circle(radius) for _ in range(numbLines)]

# Create a GeoPandas DataFrame with LineString geometry
gdf = gpd.GeoDataFrame(geometry=lines)
#gdf.head()

gdf['center_coords'] = gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
gdf['center_coords'] = [coords[0] for coords in gdf['center_coords']]
print(gdf.columns[0])
gdf['name']= ''
#gdf.plot()
#print(cars_x)
#print(cars_y)

GPP = nx.Graph()
#nid=0
#niter=0
cmap = plt.colormaps.get_cmap('tab10')
#print(cmap)
#for i1, i2 in zip(cars_x,cars_y):
    #it= len(i1)
    #eList=[]
    #for t in np.arange(0,it):
        #GPP.add_node(str(nid),pos=(i1[t],i2[t]),color=cmap(niter))
        #eList.append(str(nid))
        #nid=nid+1
    #for q in np.arange(0,len(eList)-1):
        #if( not (GPP.has_edge(eList[q],eList[q+1]) or GPP.has_edge(eList[q+1],eList[q]))):
            #GPP.add_edge(eList[q],eList[q+1])
        #deTemp= np.sqrt((i1[q]-i1[q+1])**2+(i2[q]-i2[q+1])**2)
        #if(deTemp<rth):
            #if(not GPP.has_edge(eList[q],eList[q+1])):
                #GPP.add_edge(eList[q],eList[q+1])
    #niter=niter+1
    #print(niter)

    
    
    
#GEV = nx.Graph()
#eid=0
#for i1, i2 in zip(chrgr_x,chrgr_y):
    #it= len(i1)
    #for t in np.arange(0,it):
        #GEV.add_node(str(eid),pos=(i1[t],i2[t]),color="black")
        #eList.append(str(eid))
        #eid=eid+1

    
#plt.scatter(cars_x,cars_y)
for index, row in gdf.iterrows():
        name=ABC[index]
        gdf.loc[index, "name"]= name
        #print (row["name"])
        #plt.text(row['center_coords'][0],row['center_coords'][1],name)



# First we'll need a DataFrame to hold our results
# We'll make a GeoDataFrame later
intersections_gdf = pd.DataFrame()

# Next, we'll iterate through each row in `gdf` and find out if and where it intersects with another line.
for index, row in gdf.iterrows():
    # Get GeoSeries of intersections of row with all rows
    row_intersections = gdf.intersection(row['geometry'])
    # Exclude any rows that aren't a Point geometry
    row_intersection_points = row_intersections[row_intersections.geom_type == 'Point']
    # Create a DataFrame of the the row intersection points
    row_intersections_df = pd.DataFrame(row_intersection_points)
    # Create a field for the name (or some identifying value) of the row
    row_intersections_df['name_2'] = row['name']
    # Join the input gdf to the row intersections gdf. By default, this is a left join on the index.
    # Because the row gdf is a derivative of gdf, the index of each intersecting row is the same as in gdf
    row_intersections_df = row_intersections_df.join(gdf['name'])
    # Append the row intersection gdf to results gdf
    intersections_gdf= pd.concat([intersections_gdf,row_intersections_df])

# Drop the geometry field. Because we joined directly to our input gdf, the geometry field is the Line for the feature at the joined row's index
# intersections_gdf = intersections_gdf.drop('geometry', axis = 1)
# Rename and set the point field as the geometry field
intersections_gdf = intersections_gdf.rename(columns={0: 'geometry'})
# There are two points for each intersection. We only want one. We'll create a new field to store an intersection name based on a sorted list of the name of the two intersecting lines
intersections_gdf['intersection'] = intersections_gdf.apply(lambda row: ''.join(sorted([row['name_2'], row['name']])), axis = 1)
# We'll group the intersections by their name, returning only the first result for each unique value
intersections_gdf = intersections_gdf.groupby('intersection').first()
# The index is now the intersection field. We don't want that, so we'll reset the index
intersections_gdf = intersections_gdf.reset_index()
# Finally, we'll turn the DataFrame back into a GeoDataFrame and set the CRS
intersections_gdf = gpd.GeoDataFrame(intersections_gdf, geometry = 'geometry')

intersections_gdf.set_crs(epsg="4326")

#intersections_gdf.plot( ax=ax,marker = 'o', color = 'orange', markersize = 100)
#for x, y, label in zip(intersections_gdf.geometry.x, intersections_gdf.geometry.y, intersections_gdf['intersection']):
    #ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")
    
#plt.show()
G=nx.Graph()
GPure = nx.Graph()
#display(gdf)

for index, row in gdf.iterrows():
        name=row["name"]
        x, y = row["geometry"].xy
        cur_x =  cars_x[index];
        cur_y =  cars_y[index];
        ev_x = chrgr_x[index];
        ev_y= chrgr_y[index];
        slice_inter = intersections_gdf.loc[(intersections_gdf["name"]==name)|(intersections_gdf["name_2"]==name)]
        slice_inter = slice_inter.iloc[ slice_inter.geometry.x.argsort().values]
        #display(slice_inter)
        #G.add_edge(name+"1",name+"2")
        
        pervNode= name+"1"
        lastNode= name+"2"
        mins =np.argmin(x)
        perv_x = x[mins]
        perv_y = y[mins]
        last_x = x[1-mins]
        last_y = y[1-mins]
        #print("perv")
        #print(pervNode)
        print(perv_x,perv_y)
        #print("last")
        #print(lastNode)
        print(last_x,last_y)
        G.add_node(pervNode,pos=(perv_x,perv_y),color="#d80032",type="road")
        G.add_node(lastNode,pos=(last_x,last_y),color="#6930c3",type="road")
        GPure.add_node(pervNode,pos=(perv_x,perv_y),color="#d80032",type="road")
        GPure.add_node(lastNode,pos=(last_x,last_y),color="#6930c3",type="road")
        count=1
        for index2, row2 in  slice_inter.iterrows():
           name2=row2['intersection']
           x2= row2["geometry"].x
           y2= row2["geometry"].y
           yt= G.nodes[pervNode]["pos"][1];
           xt= G.nodes[pervNode]["pos"][0];    
           wtemp=(xt-x2)**2+(yt-y2)**2
           G.add_node(name2,pos=(x2,y2),color="#8d99ae",type="roundabout")
           GPure.add_node(name2,pos=(x2,y2),color="#8d99ae",type="roundabout")
           G.add_edge(pervNode,name2,color='#d6e3f8')
           GPure.add_edge(pervNode,name2,color='#d6e3f8',weight=np.sqrt(wtemp))
           #check if there are any cars on this edge
           for t in np.arange(0,len(cur_x)):
                cx = cur_x[t]
                cy = cur_y[t]
                if(isBetween(a=[xt,yt],b=[x2,y2],c=[cx,cy]) and not G.has_node(name+"car-"+str(t))):
                   G.add_node(name+"car-"+str(t),pos=(cx,cy),color="orange",type="car")
                   G.add_edge(name+"car-"+str(t),pervNode,color='#c9e4ca')
                   G.add_edge(name+"car-"+str(t),name2,color='#c9e4ca')
                   
           #check if there are any EV Charger on this edge
           for et in np.arange(0,len(ev_x)):
                cevx = ev_x[et]
                cevy = ev_y[et]
                if(isBetween(a=[xt,yt],b=[x2,y2],c=[cevx,cevy]) and not G.has_node(name+"ev-"+str(t))):
                   G.add_node(name+"ev-"+str(t),pos=(cevx,cevy),color="magenta",type="charger")
                   G.add_edge(name+"ev-"+str(t),pervNode)
                   G.add_edge(name+"ev-"+str(t),name2)
                    
           pervNode=name2
           if(count==slice_inter.shape[0]):
            G.add_edge(pervNode,lastNode)
            wtemp2=(G.nodes[pervNode]["pos"][0]-G.nodes[lastNode]["pos"][0])**2+(G.nodes[pervNode]["pos"][1]-G.nodes[lastNode]["pos"][1])**2
            GPure.add_edge(pervNode,lastNode,weight=np.sqrt(wtemp2))
            
            #print( G.nodes[pervNode]["pos"])
            #check if there is a point in cars collection which lies between these nodes  
            for t in np.arange(0,len(cars_x[index])):
                cx = cur_x[t]
                cy = cur_y[t]
                if(isBetween(a=[xt,yt],b=[G.nodes[lastNode]["pos"][0],G.nodes[lastNode]["pos"][1]],c=[cx,cy]) and not G.has_node(name+"car-"+str(t))):
                   G.add_node(name+"car-"+str(t),pos=(cx,cy),color="orange",type="car")
                   G.add_edge(name+"car-"+str(t),lastNode,color='#c9e4ca')
                   G.add_edge(name+"car-"+str(t),pervNode,color='#c9e4ca')
            #check if there are any EV Charger on this edge
            for et in np.arange(0,len(ev_x)):
               cevx = ev_x[et]
               cevy = ev_y[et]
               if(isBetween(a=[xt,yt],b=[G.nodes[lastNode]["pos"][0],G.nodes[lastNode]["pos"][1]],c=[cevx,cevy]) and not G.has_node(name+"ev-"+str(t))):
                  G.add_node(name+"ev-"+str(t),pos=(cevx,cevy),color="magenta",type="charger")
                  G.add_edge(name+"ev-"+str(t),pervNode)
                  G.add_edge(name+"ev-"+str(t),lastNode)
           count=count+1
        if(slice_inter.shape[0]==0 ):
               G.add_edge(name+"1",name+"2",color='#d6e3f8')
               wtemp3=(G.nodes[name+"1"]["pos"][0]-G.nodes[name+"2"]["pos"][0])**2+(G.nodes[name+"1"]["pos"][1]-G.nodes[name+"2"]["pos"][1])**2
               GPure.add_edge(name+"1",name+"2",color='#d6e3f8',weight=np.sqrt(wtemp3))
               for t in np.arange(0,len(cars_x[index])):
                cx = cur_x[t]
                cy = cur_y[t]
                if(isBetween(a=[G.nodes[name+"1"]["pos"][0],G.nodes[name+"1"]["pos"][1]],b=[G.nodes[name+"2"]["pos"][0],G.nodes[name+"2"]["pos"][1]],c=[cx,cy]) and not G.has_node(name+"car-"+str(t))):
                   G.add_node(name+"car-"+str(t),pos=(cx,cy),color="orange",type="car")
                   G.add_edge(name+"car-"+str(t),name+"1",color='#c9e4ca')
                   G.add_edge(name+"car-"+str(t),name+"2",color='#c9e4ca')
                   
               for et in np.arange(0,len(ev_x)):
                   cevx = ev_x[et]
                   cevy = ev_y[et]
                   if(isBetween(a=[G.nodes[name+"1"]["pos"][0],G.nodes[name+"1"]["pos"][1]],b=[G.nodes[name+"2"]["pos"][0],G.nodes[name+"2"]["pos"][1]],c=[cevx,cevy])and not G.has_node(name+"ev-"+str(t))):
                       G.add_node(name+"ev-"+str(t),pos=(cevx,cevy),color="magenta",type="charger")
                       G.add_edge(name+"ev-"+str(t),name+"1")
                       G.add_edge(name+"ev-"+str(t),name+"2")
                       

for i in G.nodes:
    if(G.nodes[i]["type"]=="car"):
      GPP.add_node(i,pos=G.nodes[i]["pos"],color=G.nodes[i]["color"])
      for j in G.nodes:
          if(not(j==i) and (G.nodes[j]["type"]=="car") and j.startswith(i[0])):
              #print(i)
              #print(j)
              if(not GPP.has_edge(i,j)):
                  GPP.add_node(j,pos=G.nodes[j]["pos"],color=G.nodes[j]["color"])  
                  GPP.add_edge(i,j,color="red")
              


pos=nx.get_node_attributes(G,'pos')
cols = nx.get_node_attributes(G,'color').values()


fig1 = plt.figure(figsize=(50,50))
ax1 = fig1.add_subplot(121)
nx.draw(G, pos, with_labels=False,node_color=cols, node_size=50, edge_color="#e5e5e5", width=2, arrowstyle='->', arrows=True)
nx.draw_networkx_labels(G, pos, ax=ax1,verticalalignment='top',horizontalalignment="right")         # nudged labels
color2= nx.get_node_attributes(GPure,'color').values()
ax1.plot(xx0 + xp, yy0 + yp, color='k');
ax2 = fig1.add_subplot(122)
#GAll=nx.compose(G,GPP)

#edge_colors = ['#edeec9' if e in GPP.edges else "grey" for e in GAll.edges]
#weights = [6 if e in GPP.edges else 2 for e in GAll.edges]
#print(edge_colors)
#nx.draw(GAll, ax=ax2, pos=nx.get_node_attributes(GAll,'pos'), node_color=nx.get_node_attributes(GAll,'color').values(),node_shape='s',node_size=40,  arrowsize=10, arrows=True, width=2,arrowstyle='->',edge_color=edge_colors)
#nx.draw(GPP,pos=nx.get_node_attributes(GPP,'pos'), ax=ax2,node_color=list(color2),node_shape='s',node_size=40, edge_color = '#f26a8d',alpha=1, arrowsize=10, arrows=True, width=12,arrowstyle='fancy')
#nx.draw(G,pos=nx.get_node_attributes(G,'pos'),ax=ax2,node_color=cols,alpha=0.2)
ax2.plot(xx0 + xp, yy0 + yp, color='k');
nx.draw(GPure,  pos=nx.get_node_attributes(GPure,'pos'), ax=ax2, node_color=color2, node_size=50, edge_color="#e5e5e5", width=2, arrowstyle='->', arrows=True)
ax1.axis('equal')
ax2.axis('equal')
plt.savefig('PLCPEx.pdf', dpi=400)
plt.show()