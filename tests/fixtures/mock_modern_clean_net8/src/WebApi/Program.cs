var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.Decorate<IOrderService, CachedOrderService>();

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();

public interface IOrderService {}
public class OrderService : IOrderService {}
public class CachedOrderService : IOrderService 
{
    public CachedOrderService(IOrderService inner) {}
}
