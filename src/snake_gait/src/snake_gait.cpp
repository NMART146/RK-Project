#include <chrono>
#include <memory>
#include <cmath>
#include <string>
#include <vector>
#include <optional>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"


class SnakeGait : public rclcpp::Node
{
public:
  SnakeGait()
  : Node("snake_gait_publisher")
  {
    // Parameters
    this->declare_parameter<double>("beta", 0);
    this->declare_parameter<double>("a", 0.25);
    this->declare_parameter<double>("omega", M_PI/5);
    this->declare_parameter<double>("v", 2*M_PI);
    this->declare_parameter<double>("update_rate", 60);
    this->declare_parameter<std::string>("controller_topic","/snake_gait_controller/commands");
    this->declare_parameter<int>("num_joints", 9);


    beta_                   = this->get_parameter("beta").as_double();
    amp_                    = this->get_parameter("a").as_double();
    omega_                  = this->get_parameter("omega").as_double();
    v_                      = this->get_parameter("v").as_double();
    update_rate_            = this->get_parameter("update_rate").as_double();
    topic_                  = this->get_parameter("controller_topic").as_string();
    num_joints_             = this->get_parameter("num_joints").as_int();

    publisher_ = this->create_publisher<std_msgs::msg::Float64MultiArray>(topic_, 10);

    if (update_rate_ < 1) {
        update_rate_ = 60; // incase update rate is less than 1
    }

    // Timer — period derived from update rate
    auto period = std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::duration<double>(1.0 / update_rate_));
    timer_ = this->create_timer(
        period, std::bind(&SnakeGait::timer_callback, this));

  }

private:
    void timer_callback(){
        if (!start_) {
            start_ = this->get_clock()->now();
        }
        auto msg = std_msgs::msg::Float64MultiArray();
        msg.data.resize(num_joints_,0);

        double t = this->get_clock()->now().seconds() - start_->seconds();
        double theta = 0;
        for (int i = 0; i < num_joints_; i++) {
            theta = beta_ + amp_*sin(omega_ * i - v_ * t);
            msg.data[i] = theta;
        }

        // Publish header
        publisher_->publish(msg);

    }

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr publisher_;
    std::optional<rclcpp::Time> start_;
    double beta_;
    double amp_;
    double omega_;
    double v_;
    double update_rate_;
    std::string topic_;
    int num_joints_;
  
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SnakeGait>());
  rclcpp::shutdown();
  return 0;
}