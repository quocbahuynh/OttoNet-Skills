namespace ModernCleanApp.Domain.Exceptions;

public class DomainException : System.Exception
{
    public DomainException(string message) : base(message) { }
}

public class OrderAlreadyShippedException : DomainException
{
    public OrderAlreadyShippedException() : base("Cannot cancel an order that has already shipped.") { }
}
