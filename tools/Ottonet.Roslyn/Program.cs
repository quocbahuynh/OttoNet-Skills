using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace Ottonet.Roslyn;

public static class Program
{
    public static int Main(string[] args)
    {
        if (args.Length == 0)
        {
            Console.Error.WriteLine("Usage: Ottonet.Roslyn <file.cs> [--focus-method <name>] [--json] [--full]");
            return 1;
        }

        string filePath = args[0];
        string? focusMethod = null;
        bool outputJson = false;
        bool full = false;

        for (int i = 1; i < args.Length; i++)
        {
            if ((args[i] == "--focus-method" || args[i] == "-m") && i + 1 < args.Length)
            {
                focusMethod = args[++i];
            }
            else if (args[i] == "--json")
            {
                outputJson = true;
            }
            else if (args[i] == "--full")
            {
                full = true;
            }
        }

        if (!File.Exists(filePath))
        {
            Console.Error.WriteLine($"Error: File '{filePath}' does not exist.");
            return 1;
        }

        string sourceText = File.ReadAllText(filePath);
        if (full)
        {
            Console.WriteLine(sourceText);
            return 0;
        }

        SyntaxTree tree = CSharpSyntaxTree.ParseText(sourceText);
        CompilationUnitSyntax root = tree.GetCompilationUnitRoot();

        if (outputJson)
        {
            var inspector = new AstInspector();
            inspector.Visit(root);
            var json = JsonSerializer.Serialize(inspector.Classes, new JsonSerializerOptions { WriteIndented = true });
            Console.WriteLine(json);
            return 0;
        }

        var rewriter = new SkeletonRewriter(focusMethod);
        SyntaxNode newRoot = rewriter.Visit(root);
        Console.WriteLine("// [OTTONET ROSLYN AST] Synthesized via Microsoft.CodeAnalysis.CSharp with 100% Compiler Fidelity");
        Console.WriteLine(newRoot.ToFullString());
        return 0;
    }
}

public class AstInspector : CSharpSyntaxWalker
{
    public List<ClassMetadata> Classes { get; } = new();

    public override void VisitClassDeclaration(ClassDeclarationSyntax node)
    {
        ProcessType(node, "class", node.Identifier.ValueText, node.BaseList);
        base.VisitClassDeclaration(node);
    }

    public override void VisitRecordDeclaration(RecordDeclarationSyntax node)
    {
        ProcessType(node, "record", node.Identifier.ValueText, node.BaseList);
        base.VisitRecordDeclaration(node);
    }

    public override void VisitInterfaceDeclaration(InterfaceDeclarationSyntax node)
    {
        ProcessType(node, "interface", node.Identifier.ValueText, node.BaseList);
        base.VisitInterfaceDeclaration(node);
    }

    private void ProcessType(TypeDeclarationSyntax node, string kind, string name, BaseListSyntax? baseList)
    {
        var meta = new ClassMetadata
        {
            Kind = kind,
            Name = name,
            BaseTypes = baseList?.Types.Select(t => t.ToString()).ToList() ?? new List<string>()
        };

        foreach (var member in node.Members)
        {
            if (member is MethodDeclarationSyntax method)
            {
                var lineSpan = method.GetLocation().GetLineSpan();
                meta.Methods.Add(new MethodMetadata
                {
                    Name = method.Identifier.ValueText,
                    ReturnType = method.ReturnType.ToString(),
                    StartLine = lineSpan.StartLinePosition.Line + 1,
                    EndLine = lineSpan.EndLinePosition.Line + 1,
                    Modifiers = method.Modifiers.Select(m => m.ValueText).ToList()
                });
            }
            else if (member is PropertyDeclarationSyntax prop)
            {
                meta.Properties.Add(new PropertyMetadata
                {
                    Name = prop.Identifier.ValueText,
                    Type = prop.Type.ToString()
                });
            }
        }

        Classes.Add(meta);
    }
}

public class ClassMetadata
{
    public string Kind { get; set; } = "";
    public string Name { get; set; } = "";
    public List<string> BaseTypes { get; set; } = new();
    public List<MethodMetadata> Methods { get; set; } = new();
    public List<PropertyMetadata> Properties { get; set; } = new();
}

public class MethodMetadata
{
    public string Name { get; set; } = "";
    public string ReturnType { get; set; } = "";
    public int StartLine { get; set; }
    public int EndLine { get; set; }
    public List<string> Modifiers { get; set; } = new();
}

public class PropertyMetadata
{
    public string Name { get; set; } = "";
    public string Type { get; set; } = "";
}

public class SkeletonRewriter : CSharpSyntaxRewriter
{
    private readonly string? _focusMethod;

    public SkeletonRewriter(string? focusMethod)
    {
        _focusMethod = focusMethod;
    }

    public override SyntaxNode? VisitMethodDeclaration(MethodDeclarationSyntax node)
    {
        string methodName = node.Identifier.ValueText;
        bool isFocused = !string.IsNullOrEmpty(_focusMethod) &&
                         string.Equals(methodName, _focusMethod, StringComparison.OrdinalIgnoreCase);

        if (isFocused)
        {
            // Keep full fidelity body for focused method with Zoom-In banner
            var zoomComment = SyntaxFactory.Comment($"// >>> [OTTONET ZOOM-IN: FULL FIDELITY BODY OF {methodName}] <<<\n");
            var leading = node.GetLeadingTrivia().Add(zoomComment);
            return base.VisitMethodDeclaration(node.WithLeadingTrivia(leading));
        }

        if (node.Body != null)
        {
            var omittedStatement = SyntaxFactory.ParseStatement(
                "// ... [implementation omitted by Ottonet Roslyn AST | Run with --full for complete source] ...\n"
            );
            var emptyBlock = SyntaxFactory.Block(omittedStatement);
            return node.WithBody(emptyBlock).WithExpressionBody(null).WithSemicolonToken(default);
        }

        if (node.ExpressionBody != null)
        {
            var omittedStatement = SyntaxFactory.ParseStatement(
                "// ... [expression-bodied implementation omitted by Ottonet Roslyn AST] ...\n"
            );
            var emptyBlock = SyntaxFactory.Block(omittedStatement);
            return node.WithExpressionBody(null).WithSemicolonToken(default).WithBody(emptyBlock);
        }

        return base.VisitMethodDeclaration(node);
    }
}
