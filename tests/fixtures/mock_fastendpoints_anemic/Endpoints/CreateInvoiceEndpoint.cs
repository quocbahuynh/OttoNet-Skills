using FastEndpoints;

namespace FastApp.Endpoints;

public record CreateInvoiceRequest(string CustomerName, decimal Subtotal);
public record CreateInvoiceResponse(int InvoiceId, decimal Total);

public class CreateInvoiceEndpoint : Endpoint<CreateInvoiceRequest, CreateInvoiceResponse>
{
    public override void Configure()
    {
        Post("/api/invoices");
        AllowAnonymous();
    }

    public override async Task HandleAsync(CreateInvoiceRequest req, CancellationToken ct)
    {
        await SendOkAsync(new CreateInvoiceResponse(1, req.Subtotal), ct);
    }
}
