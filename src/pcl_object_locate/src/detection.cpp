#include <ros/ros.h>
// PCL specific includes
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/voxel_grid.h>
#include <iostream>


ros::Publisher pub;

void cloud_cb (sensor_msgs::PointCloud2 cloud_msg)
{
    pcl::PointCloud<pcl::PointXYZ> raw_input_cloud;
    pcl::fromROSMsg(cloud_msg, raw_input_cloud);

    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_ptr (new pcl::PointCloud<pcl::PointXYZ> (raw_input_cloud));
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_voxel_filtered (new pcl::PointCloud<pcl::PointXYZ> ());

    pcl::VoxelGrid<pcl::PointXYZ> voxel_filter;
    voxel_filter.setInputCloud (cloud_ptr);
    voxel_filter.setLeafSize (0.01f,0.01f,0.01f);
    voxel_filter.filter (*cloud_voxel_filtered);

    //TO-DO Pass through filter

    sensor_msgs::PointCloud2::Ptr output_msg(new sensor_msgs::PointCloud2);

    pcl::toROSMsg(*cloud_voxel_filtered,*output_msg);
    // Publish the data
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