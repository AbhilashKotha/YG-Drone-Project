using System;
using Microsoft.Maui.Controls;

namespace UIRemote
{
    public class stepsizecontrolsLayout : StackLayout
    {
        private int _counter = 1;

        public event EventHandler PlusButtonClick;
        public event EventHandler MinusButtonClick;

        public int Counter
        {
            get => _counter;
            set
            {
                _counter = value < 1 ? 1 : (value > 10 ? 10 : value);
                UpdateCounterLabel();
            }
        }

        private Label counterLabel;
        // Add a Label property to hold the label text
        public stepsizecontrolsLayout()
        {
            var plusButton = CreateButton("+");
            var minusButton = CreateButton("-");

            plusButton.Clicked += (s, e) => PlusButtonClick?.Invoke(this, EventArgs.Empty);
            minusButton.Clicked += (s, e) => MinusButtonClick?.Invoke(this, EventArgs.Empty);

            counterLabel = new Label
            {
                Text = _counter.ToString(),
                FontSize = 30,
                WidthRequest = 30,
                HorizontalOptions = LayoutOptions.Center,
                VerticalOptions = LayoutOptions.Center
            };
            // Add buttons and counter label to the stack layout
            Children.Add(new StackLayout
            {
                Orientation = StackOrientation.Horizontal,
                Children = { minusButton, counterLabel, plusButton }
            });

            // Set the stack layout options to center the buttons and the label
            HorizontalOptions = LayoutOptions.Center;
            VerticalOptions = LayoutOptions.Center;
        }

        private Button CreateButton(string text)
        {
            return new Button
            {
                Text = text,
                BackgroundColor = Color.FromRgb(20, 20, 20),
                WidthRequest = 50,
                HeightRequest = 50
            };
        }

        private void UpdateCounterLabel()
        {
            counterLabel.Text = _counter.ToString();
        }
    }
}
