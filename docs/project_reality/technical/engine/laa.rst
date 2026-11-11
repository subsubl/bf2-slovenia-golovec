
Updating RendDx9 to use LAA D3DX9
=================================

BF2 is compiled with the Large Address Aware (LAA) flag, allowing the process to use up to 4GB of memory. However, because RendDx9 does not use Direct3D in LAA mode, using more than 2GB of memory may cause Direct3D crashes. This tutorial demonstrates how to edit the shaders and Renddx9.dll to use LAA mode for Direct3D and utilize the full 4GB of memory.

Shader Preparation
------------------

To use the LAA flag, RendDx9 must be linked to a newer d3dx9.dll. However, newer versions no longer support shadermodel 1.3, 1.4, and 2_0x used in BF2 shaders. The first step is to prepare the shaders for shadermodel 3.0.

Cleaning Shaders
^^^^^^^^^^^^^^^^

Before converting shaders to the newer shadermodel, clean the code to reduce the amount of necessary adjustments:

#. Remove all unneeded effect files.
#. Remove all unreachable code within ``_FORCE_1_3_``, ``_FORCE_1_4_``, and ``#if 0`` branches.
#. Remove all commented-out shader code.

It is also recommended to replace DICE-specific datatypes (scalar, vector, matrix) with standard ones (float, float3, float3x3, etc.) to improve readability and documentation compatibility.

Update Existing HLSL Shadermodel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Change all existing HLSL shaders to use the newer shadermodel. This is primarily a find-and-replace task. Replace existing shadermodel definitions (e.g., ``PSMODEL`` or ``PS2_EXT``) with the defaults ``ps_3_0`` and ``vs_3_0``.

Additionally, replace all passes using the name "point" with something like ``point_`` because "point" is a predefined control word in newer DirectX versions.

Updating Inline ASM Code
^^^^^^^^^^^^^^^^^^^^^^^^

DICE used inline ASM code in many shaders to reduce instruction counts. This code is mostly written in shadermodel 1.3 or 1.4 and is not supported by newer DirectX versions. To update this, you can:

#. Update the ASM to your chosen shadermodel.
#. Rewrite the ASM in HLSL and compile it with your chosen shadermodel.

For PR, we rewrote these in HLSL. You can reference our implementation for guidance, but do not use :file:`shaders_client.zip` directly as it contains PR-specific parts. Manually copy the translated HLSL you need and credit us if you use it.

.. admonition:: Helpful Resources

   - https://docs.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl
   - https://gamedev.stackexchange.com/

Updating RendDx9.dll
--------------------

To use DirectX with LAA addresses, create effects with the `D3DXFX_LARGEADDRESSAWARE <https://docs.microsoft.com/en-us/windows/win32/direct3d9/d3dxfx>`_ flag. We edited the ShaderManager constructor to include this flag.

Because LAA prevents addressing resources by name in some cases, additional changes are required. Minor fixes, such as adjusting the D3DFORMAT for screenshots, are also necessary.

Explanation of the format:

.. code-block:: text

   [...] defines the file to edit
   A: file offset of the bytes to change
   O: Original bytes
   N: New bytes
   #: Comments

The code snippets in comments reference loaded addresses, not file offsets.

.. code-block:: text
   :caption: RendDx9.dll

   # Author: Mats
   # This sets flags in shadermanager to include 0x200000 Large address aware

   [RendDx9.dll]
   A: 241B7
   O: 38 5E 7C 74 07 83 8E 84 00 00 00 04
   N: 81 8E 84 00 00 00 00 00 02 00 90 90

   # RendDX9.dll+364C1 - 81 E2 00000200        - and edx,00020800
   [RendDx9.dll]
   A: 358C4
   O: 08 00
   N: 08 02

   RendDX9.dll+3611F - 25 00000200           - and eax,00020800
   [RendDx9.dll]
   A: 35521
   O: 08 00
   N: 08 02

   # Skipping DX9 calls with 0x0 as parameter handle. In non LAA this just return error, in LAA it crashes
   # Replace at RendDX9.dll+1E715
   # 85 C0                   - test eax, eax             ; Test for 0x0
   # 74 37                   - je RendDX9.dll+1E77E      ; Skip DX call if 0x0
   # 53                      - push ebx                  ; Push parameters
   # 50                      - push eax
   # EB 2F                   - jmp RendDX9.dll+1E74A     ; Jump Back to DX call
   #
   # Replace at RendDX9.dll+1E748
   # EB CB                   - jmp RendDX9.dll+1E715     ; Jump to Null-Check
   #
   # Replace at RendDX9.dll+1E542
   # 85 C0                   - test eax, eax             ; Test for 0x0
   # 74 06                   - je RendDX9.dll+1E54C      ; Jump to pop
   # 50                      - push eax                  ; Push parameter
   # 8B 46 08                - mov eax, [esi+08]         ; Get last parameter
   # EB B2                   - jmp RendDX9.dll+1E4FE     ; Jump Back to DX call
   # 58                      - pop eax                   ; 2 parameter got pushed before
   # 58                      - pop eax                   ; pop those into eax to discard
   # EB B2                   - jmp RendDX9.dll+1E502
   #
   # Replace at RendDX9.dll+1E4FA
   # EB 46                   - jmp RendDX9.dll+1E542     ; Jump to Null-Check
   # 90                      - NOP
   # 90                      - NOP

   [RendDx9.dll]
   A: 1DB48
   O: 53 50
   N: EB CB

   [RendDx9.dll]
   A: 1DB13
   O: CC CC CC CC CC CC CC CC
   N: 85 C0 74 37 53 50 EB 2F

   [RendDx9.dll]
   A: 1D8FA
   O: 50 8B 46 08
   N: EB 46 90 90

   [RendDx9.dll]
   A: 1D942
   O: CC CC CC CC CC CC CC CC CC CC CC CC CC CC
   N: 85 C0 74 06 50 8B 46 08 EB B2 58 58 EB B2

   # Passing handle instead of name into DX9 call
   # Replace at RendDX9.dll+4C1D9
   # E9 B6 E6 18 00          - jmp RendDX9.dll+1DA894    ; Jump to code cave to use correct parameters
   #
   # 52                      - push edx
   # 8B 95 54 FF FF FF       - mov edx,[ebp-000000AC]    ; Get Handle instead of name
   # 52                      - push edx
   # E9 3D 19 E7 FF          - jmp RendDX9.dll+4C1DE     ; Back to DX call

   [RendDx9.dll]
   A: 4B5D9
   O: 52 8B 55 F8 52
   N: E9 B6 E6 18 00

   [RendDx9.dll]
   A: 1D9C94
   O: 00 00 00 00 00 00 00 00 00 00 00 00 00
   N: 52 8B 95 54 FF FF FF 52 E9 3D 19 E7 FF

   # Changing screenshot D3DFORMAT from D3DFMT_A8R8G8B8 to D3DFMT_X8R8G8B8 as otherwise .png one has alpha in it
   # This might reduce quality of screenshots
   [RendDx9.dll]
   A: 458B
   O: 15
   N: 16

After these steps, replace :file:`d3dx9_25.dll` with :file:`d3dx9_43.dll` (the latest DirectX 9). BF2 also loads :file:`d3dx9_24.dll` dynamically to fix an obscure bug; this should still function correctly. Using :file:`d3dx9_43.dll` may cause crashes, while :file:`d3dx9_24.dll` does not appear to cause further issues with high memory.

Updating TextureAtlasBuilder.dll and bf2.exe
--------------------------------------------

These steps are optional but recommended. For :file:`TextureAtlasBuilder.dll`, change :file:`d3dx9_25.dll` to :file:`d3dx9_43.dll`. This reduces the number of different ``d3dx9`` versions loaded.

For :file:`bf2.exe`, it is recommended to apply a fix for loading minimap icons with addresses above the 2GB memory space.

.. code-block:: text
   :caption: bf2.exe

   # Author: Mats
   # This fixes flags and other icons starting to become missing when high on memory

   # Change
   # From: prbf2_repo.exe+3746F2 - 0F8E 93010000         - jng prbf2_repo.exe+37488B
   # To:   prbf2_repo.exe+3746F2 - 0F84 93010000         - je prbf2_repo.exe+37488B
   [bf2.exe]
   A: 373AF3
   O: 8E
   N: 84

Issues to be Aware of
---------------------

These changes are included in the current PR and have been tested on various systems, making them generally stable. However, players using graphics mods like Reshade or overlays like Overwolf may experience crashes as these tools may no longer work with the updated shaders and ``d3dx9``.
