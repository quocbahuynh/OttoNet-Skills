namespace FastApp.Services;

public class Invoice
{
    public int Id { get; set; }
    public string Status { get; set; } = "Draft";
    public decimal TotalAmount { get; set; }
}

public class InvoiceService
{
    private readonly ITaxClient _taxClient;

    public InvoiceService(ITaxClient taxClient)
    {
        _taxClient = taxClient;
    }

    public async Task<Invoice> ProcessInvoice(decimal subtotal)
    {
        // Semantic calculation equation
        decimal taxRate = await _taxClient.GetRateAsync();
        decimal total = subtotal * (1 + taxRate) + 5.50m;
        
        var invoice = new Invoice();
        invoice.Status = "Approved";
        invoice.TotalAmount = total;
        return invoice;
    }
}

public interface ITaxClient
{
    Task<decimal> GetRateAsync();
}
