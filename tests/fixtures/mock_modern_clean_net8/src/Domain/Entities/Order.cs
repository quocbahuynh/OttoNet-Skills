namespace ModernCleanApp.Domain.Entities;

public enum OrderStatus
{
    Draft,
    Submitted,
    Processing,
    Shipped,
    Cancelled
}

public class Order
{
    public int Id { get; private set; }
    public int CustomerId { get; private set; }
    public OrderStatus Status { get; private set; }
    public decimal TotalAmount { get; private set; }
    public ICollection<OrderItem> Items { get; private set; } = new List<OrderItem>();

    public void Cancel()
    {
        if (Status == OrderStatus.Shipped)
        {
            throw new InvalidOperationException("Cannot cancel an order that has already shipped.");
        }
        Status = OrderStatus.Cancelled;
    }
}
