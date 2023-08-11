using Microsoft.Maui.Controls;
using Microsoft.Maui.Controls.Compatibility;
using System.Diagnostics.Metrics;

namespace UIRemote
{
    public partial class SettingsPage : ContentPage
    {
        public int ThrottleCounter { get; set; }
        public int PitchCounter { get; set; }
        public int YawCounter { get; set; }
        public int RollCounter { get; set; }

        public SettingsPage()
        {
            InitializeComponent();

            // Create instances of the stepsizecontrolsLayout for each counter
            var throttleLayout = new stepsizecontrolsLayout();
            var pitchLayout = new stepsizecontrolsLayout();
            var yawLayout = new stepsizecontrolsLayout();
            var rollLayout = new stepsizecontrolsLayout();
            // Bind the counters of each layout to the corresponding properties in the code-behind
            throttleLayout.Counter = ThrottleCounter;
            pitchLayout.Counter = PitchCounter;
            yawLayout.Counter = YawCounter;
            rollLayout.Counter = RollCounter;

            // Subscribe to the PlusButtonClick and MinusButtonClick events for each layout
            throttleLayout.PlusButtonClick += (s, e) =>
            {
                ThrottleCounter++;
                throttleLayout.Counter = ThrottleCounter;
            };

            throttleLayout.MinusButtonClick += (s, e) =>
            {
                ThrottleCounter--;
                throttleLayout.Counter = ThrottleCounter;
            };

            pitchLayout.PlusButtonClick += (s, e) =>
            {
                PitchCounter++;
                pitchLayout.Counter = PitchCounter;
            };

            pitchLayout.MinusButtonClick += (s, e) =>
            {
                PitchCounter--;
                pitchLayout.Counter = PitchCounter;
            };

            yawLayout.PlusButtonClick += (s, e) =>
            {
                YawCounter++;
                yawLayout.Counter = YawCounter;
            };

            yawLayout.MinusButtonClick += (s, e) =>
            {
                YawCounter--;
                yawLayout.Counter = YawCounter;
            };

            rollLayout.PlusButtonClick += (s, e) =>
            {
                RollCounter++;
                rollLayout.Counter = RollCounter;
            };

            rollLayout.MinusButtonClick += (s, e) =>
            {
                RollCounter--;
                rollLayout.Counter = RollCounter;
            };

            // Add the layouts to the StackLayout in the Content of the SettingsPage
            settingsStack1.Children.Add(new Label
            {
                Text = "Throttle",
                FontSize = 20,
                FontAttributes = FontAttributes.Bold,
                HorizontalOptions = LayoutOptions.Center
            });
            settingsStack1.Children.Add(throttleLayout);
            settingsStack1.Children.Add(new Label
            {
                Text = "Pitch",
                FontSize = 20,
                FontAttributes = FontAttributes.Bold,
                HorizontalOptions = LayoutOptions.Center
            });
            settingsStack1.Children.Add(pitchLayout);
            settingsStack2.Children.Add(new Label
            {
                Text = "Yaw",
                FontSize = 20,
                FontAttributes = FontAttributes.Bold,
                HorizontalOptions = LayoutOptions.Center
            });
            settingsStack2.Children.Add(yawLayout);
            settingsStack2.Children.Add(new Label
            {
                Text = "Roll",
                FontSize = 20,
                FontAttributes = FontAttributes.Bold,
                HorizontalOptions = LayoutOptions.Center
            });
            settingsStack2.Children.Add(rollLayout);
        }
    }
}
