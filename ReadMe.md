## Modern Assembly

- Registers
  - 0-7 Used to pass the first eight integer or pointer arguments to a function. If there are more, the stack is used. Also used to return values.
  - 8 Used for indirect return value addresses or as a temporary register.
  - 9-15 Volatile/caller-saved registers, meaning the caller function must save their values if needed across a function call. Used for general-purpose temporary storage.
  - 16-17 Used for inter-procedure linkage, often by the dynamic linker/loader.
  - 18 Platform register; its use may vary by OS.
  - 19-28 Non-volatile/callee-saved registers. The called function (callee) is responsible for preserving their values before using them and restoring them before returning.
  - 29 Frame Pointer (FP), used to manage stack frames.
  - 30 Link Register (LR), holds the return address of a function call.
  - sp Stack Pointer, points to the top of the current stack frame.

- Variable Declaration
    
    ```jsx
    reg x: int8 @ x0
	x = 5

	// or

	reg y: uint8 @ x1 = 5
    ```
    
- Types
    
    ```jsx
    int8 (-128 to 127)
    uint8 (0 to 255)
    ```
    
- Arithmetic
    
    ```jsx
    add(x, y)
    sub()

    reg result: int8 @ x1 = add(x, y)
    ```
    
- Built ins
    
    ```jsx
    print() // bl _printf
    ```
    
- future ideas
    
    ```jsx
    move x->y (not copy but move value from x to y and clear x)
    clear x (zeros out register)
    
    // later this will be used for stack and heap
    stack b: int @ -8
    heap p: ptr @ alloc(32)

    // some way to potentially move a value from reg to stack/heap
    mov(to, from) (x, y)

    // debug
    debug(assembly)
    debug(registers)
    debug(x9)
    ```

Tokens -> Lexer -> AST Nodes -> Parser -> Semantic Analyzer -> codegen
Errors (central location for error handling)
Utils (for shared functions across )
Driver (the end to end process to run)



generate assembly
cd compiler/examples
python3 test.py

assemble
cd ../build
as -o output.o output.s
ld -o program output.o -lSystem -syslibroot `xcrun -sdk macosx --show-sdk-path` -e _main -arch arm64

run
./program