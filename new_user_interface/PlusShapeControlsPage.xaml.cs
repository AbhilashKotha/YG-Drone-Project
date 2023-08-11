using System.Numerics;

namespace UIRemote
{
    public partial class PlusShapeControlsPage : ContentPage
    {
        private Vector2 center;
        private Vector2 initialPosition;
        private Vector2 center2;
        private Vector2 initialPosition2;
        public PlusShapeControlsPage()
        {
            InitializeComponent();
            // Get the center position of the big circle
            center = new Vector2((float)(bigCircle.Width / 2), (float)(bigCircle.Height / 2));
            center2 = new Vector2((float)(bigCircle2.Width / 2), (float)(bigCircle2.Height / 2));
            // Set the initial position of the small circle to the center
            smallCircle.TranslationX = center.X;
            smallCircle.TranslationY = center.Y;
            smallCircle2.TranslationX = center2.X;
            smallCircle2.TranslationY = center2.Y;
        }
        private async void OnPanUpdated(object sender, PanUpdatedEventArgs e)
        {
            switch (e.StatusType)
            {
                case GestureStatus.Started:
                    // Save the initial position of the small circle
                    initialPosition = new Vector2((float)smallCircle.TranslationX, (float)smallCircle.TranslationY);
                    break;
                case GestureStatus.Running:
                    // Move the small circle within the big circle
                    var newX = initialPosition.X + (float)e.TotalX;
                    var newY = initialPosition.Y + (float)e.TotalY;
                    var distance = Vector2.Distance(center, new Vector2(newX, newY));
                    if (distance <= 100) // 150 is half of the big circle's width
                    {
                        smallCircle.TranslationX = newX;
                        smallCircle.TranslationY = newY;
                    }
                    break;
                case GestureStatus.Completed:
                case GestureStatus.Canceled:
                    // Snap the small circle back to the center
                    await SnapToCenterAsync();
                    break;
            }
        }
        private async void OnPanUpdated2(object sender, PanUpdatedEventArgs e)
        {
            switch (e.StatusType)
            {
                case GestureStatus.Started:
                    // Save the initial position of the small circle
                    initialPosition2 = new Vector2((float)smallCircle2.TranslationX, (float)smallCircle2.TranslationY);
                    break;
                case GestureStatus.Running:
                    // Move the small circle within the big circle
                    var newX = initialPosition2.X + (float)e.TotalX;
                    var newY = initialPosition2.Y + (float)e.TotalY;

                    currentValueLabel.Text = $"{newX} and {newY}";

                    var distance = Vector2.Distance(center2, new Vector2(newX, newY));
                    if (distance <= 100) // 150 is half of the big circle's width
                    {
                        smallCircle2.TranslationX = newX;
                        smallCircle2.TranslationY = newY;
                    }
                    break;
                case GestureStatus.Completed:
                case GestureStatus.Canceled:
                    // Snap the small circle back to the center
                    await SnapToCenterAsync2();
                    break;
            }
        }

        private async Task SnapToCenterAsync()
        {
            await smallCircle.TranslateTo(center.X, center.Y, 1000, Easing.SpringOut);
        }
        private async Task SnapToCenterAsync2()
        {
            await smallCircle2.TranslateTo(center2.X, center2.Y, 1000, Easing.SpringOut);
        }
    }
}
