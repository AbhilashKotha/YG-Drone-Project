using System;
using Microsoft.Maui.Controls;

namespace UIRemote
{
    public class PlusLayout : StackLayout
    {
        public event EventHandler TopButtonClick;
        public event EventHandler RightButtonClick;
        public event EventHandler BottomButtonClick;
        public event EventHandler LeftButtonClick;

        public PlusLayout()
        {

            var topButton = CreateArrowButton("up2.svg");
            var rightButton = CreateArrowButton("right2.svg");
            var bottomButton = CreateArrowButton("bottom2.svg");
            var leftButton = CreateArrowButton("left2.svg");
            var circleinmiddle = CreateArrowButton("round1.svg");

            topButton.Clicked += (s, e) => TopButtonClick?.Invoke(this, EventArgs.Empty);
            rightButton.Clicked += (s, e) => RightButtonClick?.Invoke(this, EventArgs.Empty);
            bottomButton.Clicked += (s, e) => BottomButtonClick?.Invoke(this, EventArgs.Empty);
            leftButton.Clicked += (s, e) => LeftButtonClick?.Invoke(this, EventArgs.Empty);


            // Add buttons to the stack layout
            Children.Add(topButton);
            Children.Add(new StackLayout
            {
                Orientation = StackOrientation.Horizontal,
                Children = { leftButton, circleinmiddle, rightButton }
            });
            Children.Add(bottomButton);

            // Set the stack layout options to center the buttons
            HorizontalOptions = LayoutOptions.Center;
            VerticalOptions = LayoutOptions.Center;
        }

        private ImageButton CreateArrowButton(string imageSource)
        {
            return new ImageButton
            {
                Source = imageSource,
                BackgroundColor = Color.FromRgba(20,20,20,0),
                Aspect = Aspect.AspectFit,
                WidthRequest = 50,
                HeightRequest = 50
            };
        }
    }
}
