## Modern Assembly

- Registers
  - 0-7 Used to pass the first eight integer or pointer arguments to a function. If there are more, the stack is used. Also used to return values (x0 for single values, x0-x1 for 128-bit values).
  - 8 Used for indirect return value addresses or as a temporary register.
    - using for stack allocation to avoid overwritting any general registers
    - ARM doesn't allow direct to stack , must store value in register first
  - 9-15 Volatile/caller-saved registers, meaning the caller function must save their values if needed across a function call. Used for general-purpose temporary storage.
  - 16-17 Used for inter-procedure linkage, often by the dynamic linker/loader.
    - 16 used for syscalls on macOS (Darwin-specific extension)
  - 18 Platform register; its use may vary by OS.
  - 19-28 Non-volatile/callee-saved registers. The called function (callee) is responsible for preserving their values before using them and restoring them before returning.
  - 29 Frame Pointer (FP), used to manage stack frames and point to the current function's stack frame base.
  - 30 Link Register (LR), holds the return address of a function call (where to return after function completes).
  - 31 Can be used as Stack Pointer (SP) or Zero Register (XZR/WZR) depending on context.
  - sp Stack Pointer, points to the top of the current stack frame (lowest address, stack grows downward).
    - is updated automatically as memory is allocated for the stack
  - pc Program counter, track which instruction to execute

Memory 

Stack
- Fast: just adjust stack pointer
- Automatic - cleaned up when function returns
- fixed size: known at compile time
- limited scope: only lives during function
- limited size: stack overflow if too big
- 1 allocation per function, must be deallocated at the end
- In arm, stack is set by subtracting, going down
Heap
- flixible size: allocated at runtime
- ling lived: exists until you free it
- large allocations: megabytes/gigabytes
- slower: syscall overhead
- manual management: must free or leak memory

Memory Address Layout (ARM64 macOS typical):

0xFFFFFFFF_FFFFFFFF  ← High memory (top)
    |
    | [Kernel space]
    |
0x00007FFF_FFFFFFFF
    |
    | [Stack grows DOWN ↓]
    | [Your variables here]
    | sp → [Current top of stack]
    |
    |     ... (unused space)
    |
    | [Heap grows UP ↑]
    | [Dynamic allocations]
    |
    | [Data segment] (.data, .bss)
    | [Code segment] (.text)
    |
0x00000001_00000000  ← Low memory (bottom)

sp → 0x0FF0  ┌─────────────┐  ← Each row is ONE offset
      +0     │     5       │  ← 4 bytes (bytes 0-3)
      +4     │             │  ← 4 bytes (bytes 4-7)
      +8     │             │  ← 4 bytes (bytes 8-11)
      +12    │             │  ← 4 bytes (bytes 12-15)
      0x1000 └─────────────┘

Caller's frame:
      ┌─────────────┐
      │ caller vars │
      ├─────────────┤ ← Caller's x29 points here
      │  saved x29  │
      │  saved x30  │
      ├─────────────┤ ← Current sp (our x29)
Your frame:
      │  var a      │ ← [x29, #-16] or [sp, #0]
      │  var b      │ ← [x29, #-12] or [sp, #4]
      │  var c      │ ← [x29, #-8]  or [sp, #8]
sp →  └─────────────┘

// Stack: Direct access
alloc(stack, 32)
stack x: int8 = 5

// Heap: Pointer-based (shows what's really happening)
heap y: ptr = alloc(heap, 64)
store(y, 5)
value = load(y)
free(heap, y)

- Variable Declaration
    
    ```jsx
    // register
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
    stack b: int8 = 5
    heap a: int8 = 5;            // Allocates 4 bytes (aligned int8)
    heap arr: int8[32]; 

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

TODO:

HIGH PRIORITY (Foundation):
- comments (easy, do this anytime!)
- if/else
- loops (while, for)
- comparison operators (==, !=, <, >, <=, >=)
- boolean operators (and, or, not)
- functions + return (do together)

MEDIUM PRIORITY (More Features):
- rest of arithmetic operators (-, *, /, %)
- arrays
- strings
- heap allocation/free

LOW PRIORITY (Advanced):
- structs
- pointers (if not done with heap)
- register spilling (when you run out of registers)
- move semantics
- copy semantics

OPTIMIZATION (Much Later):
- register allocation optimization
- dead code elimination
- constant folding

