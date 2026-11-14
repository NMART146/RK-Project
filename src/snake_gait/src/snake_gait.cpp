#include <chrono>
#include <memory>
#include <cmath>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/header.hpp"


class SnakeGait : public rclcpp::Node
{
public:
  SnakeGait()
  : Node("snake_gait_publisher")
  {
    // Parameters
    this->declare_parameter<double>("Beta", 0);
    this->declare_parameter<double>("A", 0.25);
    this->declare_parameter<double>("Omega", PI/5);
    this->declare_parameter<double>("v", 2*PI);
    this->declare_parameter<double>("update_rate", 60);
    this->declare_parameter<string>("controller_topic","");
    this->declare_parameter<int>("num_joints", 9);


    beta_                   = this->get_parameter("beta").as_double();
    A_                      = this->get_parameter("A").as_double();
    Omega_                  = this->get_parameter("Omega").as_double();
    v_                      = this->get_parameter("v").as_double();
    update_rate_            = this->get_parameter("update_rate").as_double();
    std::string topic_      = this->get_parameter("controller_topic").as_string();
    num_joints_             = this->get_parameter("num_joints").as_int();

    publisher_ = this->create_publisher<std_msgs::msg::Float64MultiArray>(topic, 10);

    // Timer — period derived from update rate
    auto period = std::chrono::duration_cast<std::chrono::nanoseconds>(
      std::chrono::duration<double>(1.0 / update_rate));
    timer_ = this->create_wall_timer(
      period, std::bind(&SnakeGait::timer_callback, this));

  }

private:
    void timer_callback(){
        // Capture timestamp at the rising edge
        auto msg = std_msgs::msg::Float64MultiArray();

        double theta = 0;
        for (int i = 0; i < num_joints_; i++) {
            theta = Beta_ + Amp_*sin(omega_ * i + v_ * (this->get_clock()->now().seconds()));
            msg.data(i) = theta;
        }

        // Publish header
        publisher_->publish(msg);

    }

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr publisher_;
    double beta_;
    double A_;
    double Omega_;
    double v_;
    double update_rate_;
    string topic_;
    int num_joints_;
  
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SnakeGait>());
  rclcpp::shutdown();
  return 0;
}