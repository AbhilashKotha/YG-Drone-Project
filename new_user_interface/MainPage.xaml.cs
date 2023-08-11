using Microsoft.EntityFrameworkCore.Query.Internal;
using System.Text;
using System.Text.Json;

namespace UIRemote
{
    public partial class MainPage : ContentPage
    {
        private readonly HttpClient client;
        private int throttle_percentage = 0;
        private int throttle_step_size = 1 ;
        private int rudder_percentage = 0  ;
        private int rudder_step_size = 1   ;
        private int elevator_percentage = 0;
        private int elevator_step_size = 1 ;
        private int aileron_percentage =0  ;
        private int aileron_step_size = 1;
        public MainPage()
        {
            client = new HttpClient();
            client.BaseAddress = new Uri("http://10.0.2.2:8000");
            InitializeComponent();
        }

        private void TopButton_Clicked(object sender, System.EventArgs e)
        {
            throttle_percentage += throttle_step_size;
            SendRequestAsync("set_throttle", throttle_percentage);
        }

        private void RightButton_Clicked(object sender, System.EventArgs e)
        {
            rudder_percentage += rudder_step_size;
            SendRequestAsync("set_rudder", rudder_percentage);
        }

        private void BottomButton_Clicked(object sender, System.EventArgs e)
        {
            throttle_percentage -= throttle_step_size;
            SendRequestAsync("set_throttle", throttle_percentage);
        }

        private void LeftButton_Clicked(object sender, System.EventArgs e)
        {
            rudder_percentage -= rudder_step_size;
            SendRequestAsync("set_rudder", rudder_percentage);
        }
        private void TopButton2_Clicked(object sender, System.EventArgs e)
        {
            elevator_percentage += elevator_step_size;
            SendRequestAsync("set_elevator", elevator_percentage);
        }

        private void RightButton2_Clicked(object sender, System.EventArgs e)
        {
            aileron_percentage += aileron_step_size;
            SendRequestAsync("set_aileron", aileron_percentage);
        }

        private void BottomButton2_Clicked(object sender, System.EventArgs e)
        {
            elevator_percentage -= elevator_step_size;
            SendRequestAsync("set_elevator", elevator_percentage);
        }

        private void LeftButton2_Clicked(object sender, System.EventArgs e)
        {
            aileron_percentage -= aileron_step_size;
            SendRequestAsync("set_aileron", aileron_percentage);
        }
        private void ArmButtonClicked(object sender, System.EventArgs e)
        {
            // Handle right button click
            // DisplayAlert("Right Button", "arm button clicked!", "OK");
            SendRequestAsync("arm_drone");
        }
        private void DisarmButtonClicked(object sender, System.EventArgs e)
        {
            // Handle right button click
            SendRequestAsync("disarm_drone");
        }
        public async Task SendRequestAsync(string route, int? value = null)
        {
            try
            {
                
                var url = $"{client.BaseAddress}/{route}";
                object data = null;
                if (value != null)
                {
                    data = new Dictionary<string, int>
                {
                    { route, value.Value }
                };
                }

                string jsonData = JsonSerializer.Serialize(data);

                var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

                HttpResponseMessage response = await client.PostAsync(url, content);

                if (response.IsSuccessStatusCode)
                {
                    var responseJson = await response.Content.ReadAsStringAsync();

                    string message = responseJson ?? "Error: Invalid server response";
                }
                else
                {
                    Console.WriteLine($"Failed request to {route}. Response code: {response.StatusCode}");
                }
            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine($"Error connecting to server: {ex.Message}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }
}
public class ResponseModel
{
    public string Message { get; set; }
    public int Altitude { get; set; }
    public int Pitch { get; set; }
    public int Roll { get; set; }
    public int Yaw { get; set; }
}
