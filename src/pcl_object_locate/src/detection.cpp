#include <ros/ros.h>
// PCL specific includes
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/filters/passthrough.h>
#include <iostream>

float voxel_leaf_szie = 0.01; //in terms of meter
int z_pass_min = -1;          //in terms of meter
int z_pass_max = 1;           //in terms of meter
  
ros::Publisher pub;

void cloud_cb (sensor_msgs::PointCloud2 cloud_msg)
{
    //Create a new point cloud for storing raw input
    pcl::PointCloud<pcl::PointXYZ> raw_input_cloud;
    pcl::fromROSMsg(cloud_msg, raw_input_cloud);

    //1. VOXEL GRID FILTER [START]
    //Pointer for raw input and output of voxel filter
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_ptr (new pcl::PointCloud<pcl::PointXYZ> (raw_input_cloud));
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_voxel_filtered (new pcl::PointCloud<pcl::PointXYZ> ());

    pcl::VoxelGrid<pcl::PointXYZ> voxel_filter;
    voxel_filter.setInputCloud (cloud_ptr);
    voxel_filter.setLeafSize (voxel_leaf_szie,voxel_leaf_szie,voxel_leaf_szie);
    voxel_filter.filter (*cloud_voxel_filtered);
    //1. VOXEL GRID FILTER [END]

    //2. PASS THROUGH FILTER [START]
    //Create a new point cloud for storing filter output
    pcl::PointCloud<pcl::PointXYZ> zf_cloud;
    pcl::PointCloud<pcl::PointXYZ>::Ptr passz_cloud_ptr(new pcl::PointCloud<pcl::PointXYZ>(zf_cloud));

    pcl::PassThrough<pcl::PointXYZ> pass_z;
    pass_z.setInputCloud(cloud_voxel_filtered);
    pass_z.setFilterFieldName("z");
    pass_z.setFilterLimits(z_pass_min,z_pass_max);
    pass_z.filter(zf_cloud);
    //2. PASS THROUGH FILTER [END]

    // Publish the data
    sensor_msgs::PointCloud2::Ptr output_msg(new sensor_msgs::PointCloud2);
    pcl::toROSMsg(zf_cloud,*output_msg);

    pub.publish (output_msg);
}

int main (int argc, char** argv)
{
    // Initialize ROS
    ros::init (argc, argv, "my_pcl_tutorial");
    ros::NodeHandle nh;

    // Create a ROS subscriber for the input point cloud
    ros::Subscriber sub = nh.subscribe ("input", 1, cloud_cb);

    // Create a ROS publisher for the output point cloud
    pub = nh.advertise<sensor_msgs::PointCloud2> ("downsample_output", 1);
    
    std::cout << "hello";
    
    // Spin
    ros::spin ();
}